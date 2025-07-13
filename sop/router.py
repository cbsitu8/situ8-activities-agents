from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
import os
import tempfile
import uuid
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from sop.models import (
    FileUploadResponse, 
    SOPProcessingStatus, 
    ProcessedSOP,
    SOPSearchResult
)
from sop.document_reader import DocumentReader
from sop.sop_extractor import SOPExtractor
from sop.vector_indexer import VectorIndexer

logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/sop", tags=["sop"])

# Global instances
document_reader = DocumentReader()
sop_extractor = SOPExtractor()
vector_indexer = VectorIndexer()

# In-memory job tracking (in production, use Redis or database)
processing_jobs: Dict[str, SOPProcessingStatus] = {}

@router.get("/")
async def sop_transformer_page():
    """Serve the SOP transformer page."""
    try:
        logger.info("SOP transformer page accessed")
        
        file_path = 'static/sop-transformer.html'
        if not os.path.exists(file_path):
            logger.error(f"SOP transformer file not found: {file_path}")
            raise HTTPException(status_code=404, detail="SOP transformer page not found")
        
        logger.info(f"Serving SOP transformer file: {file_path}")
        return FileResponse(file_path)
    except Exception as e:
        logger.error(f"Error serving SOP transformer page: {str(e)}")
        raise HTTPException(status_code=500, detail=f"SOP transformer page error: {str(e)}")

@router.post("/upload", response_model=FileUploadResponse)
async def upload_sop_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Upload and process a single SOP document (.docx or .md)
    Accepts only one file at a time with 2MB size limit
    """
    try:
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        logger.info(f"Processing file upload: {file.filename} (Job: {job_id})")
        
        # Validate file type
        if not document_reader.is_supported_file(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Supported types: {', '.join(document_reader.supported_extensions)}"
            )
        
        # Check file size (FastAPI UploadFile doesn't have size directly)
        # We'll check when we save the file
        
        # Create temporary file
        temp_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_dir, file.filename)
        
        try:
            # Save uploaded file
            content = await file.read()
            
            # Check file size
            if len(content) > document_reader.max_file_size:
                raise HTTPException(
                    status_code=400,
                    detail=f"File size {len(content)} bytes exceeds maximum allowed size of {document_reader.max_file_size} bytes"
                )
            
            with open(temp_file_path, 'wb') as f:
                f.write(content)
            
            # Create initial job status
            job_status = SOPProcessingStatus(
                job_id=job_id,
                status="uploaded",
                filename=file.filename,
                file_size=len(content),
                progress=10,
                message="File uploaded successfully, starting processing..."
            )
            
            processing_jobs[job_id] = job_status
            
            # Start background processing
            background_tasks.add_task(
                process_sop_file,
                job_id=job_id,
                file_path=temp_file_path,
                filename=file.filename
            )
            
            # Return response
            response = FileUploadResponse(
                job_id=job_id,
                filename=file.filename,
                file_size=len(content),
                file_type=os.path.splitext(file.filename.lower())[1],
                status="processing",
                message="File uploaded successfully and processing started"
            )
            
            logger.info(f"File upload successful: {file.filename} (Job: {job_id})")
            return response
            
        except Exception as e:
            # Clean up temp file on error
            try:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
                os.rmdir(temp_dir)
            except:
                pass
            raise e
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/process/{job_id}", response_model=SOPProcessingStatus)
async def get_processing_status(job_id: str):
    """Get processing status for a job"""
    if job_id not in processing_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return processing_jobs[job_id]

@router.get("/results", response_model=List[Dict[str, Any]])
async def get_all_sops():
    """Get all processed SOPs"""
    try:
        sops = vector_indexer.get_all_sops()
        logger.info(f"Retrieved {len(sops)} SOPs")
        return sops
    except Exception as e:
        logger.error(f"Error retrieving SOPs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving SOPs: {str(e)}")

@router.delete("/{sop_id}")
async def delete_sop(sop_id: str):
    """Delete an SOP from the database"""
    try:
        success, error = vector_indexer.delete_sop(sop_id)
        if not success:
            raise HTTPException(status_code=404, detail=error)
        
        logger.info(f"SOP {sop_id} deleted successfully")
        return {"message": f"SOP {sop_id} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting SOP {sop_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting SOP: {str(e)}")

@router.get("/search")
async def search_sops(
    query: str,
    n_results: int = 3,
    similarity_threshold: float = 0.7
) -> List[SOPSearchResult]:
    """Search SOPs using semantic similarity"""
    try:
        if not query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        results = vector_indexer.search_sops(
            query=query,
            n_results=n_results,
            similarity_threshold=similarity_threshold
        )
        
        logger.info(f"SOP search for '{query}' returned {len(results)} results")
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching SOPs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.get("/stats")
async def get_sop_statistics():
    """Get SOP database statistics"""
    try:
        stats = vector_indexer.get_database_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting SOP stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting statistics: {str(e)}")

# Background processing function
async def process_sop_file(job_id: str, file_path: str, filename: str):
    """Background task to process SOP file"""
    try:
        logger.info(f"Starting background processing for job {job_id}")
        
        # Update status
        processing_jobs[job_id].status = "extracting_text"
        processing_jobs[job_id].progress = 25
        processing_jobs[job_id].message = "Extracting text from document..."
        
        # Extract text from document
        text_content, error = document_reader.extract_text(file_path)
        if error:
            processing_jobs[job_id].status = "failed"
            processing_jobs[job_id].error = error
            processing_jobs[job_id].message = f"Text extraction failed: {error}"
            return
        
        # Update status
        processing_jobs[job_id].status = "extracting_structure"
        processing_jobs[job_id].progress = 50
        processing_jobs[job_id].message = "Extracting SOP structure using AI..."
        
        # Extract SOP structure
        document_title = os.path.splitext(filename)[0]
        processed_sop, error = sop_extractor.extract_sop_structure(
            text_content, document_title, filename
        )
        if error:
            processing_jobs[job_id].status = "failed"
            processing_jobs[job_id].error = error
            processing_jobs[job_id].message = f"Structure extraction failed: {error}"
            return
        
        # Validate extraction
        valid, validation_error = sop_extractor.validate_extraction(processed_sop)
        if not valid:
            processing_jobs[job_id].status = "failed"
            processing_jobs[job_id].error = validation_error
            processing_jobs[job_id].message = f"Validation failed: {validation_error}"
            return
        
        # Update status
        processing_jobs[job_id].status = "indexing"
        processing_jobs[job_id].progress = 75
        processing_jobs[job_id].message = "Creating vector embeddings and storing in database..."
        
        # Index in vector database
        success, error = vector_indexer.index_sop(processed_sop)
        if not success:
            processing_jobs[job_id].status = "failed"
            processing_jobs[job_id].error = error
            processing_jobs[job_id].message = f"Indexing failed: {error}"
            return
        
        # Complete processing
        processing_jobs[job_id].status = "completed"
        processing_jobs[job_id].progress = 100
        processing_jobs[job_id].message = "SOP processing completed successfully"
        processing_jobs[job_id].result = processed_sop
        processing_jobs[job_id].completed_at = datetime.now()
        
        logger.info(f"Successfully completed processing for job {job_id}")
        
    except Exception as e:
        logger.error(f"Error in background processing for job {job_id}: {str(e)}")
        processing_jobs[job_id].status = "failed"
        processing_jobs[job_id].error = str(e)
        processing_jobs[job_id].message = f"Processing failed: {str(e)}"
        
    finally:
        # Clean up temporary file
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                # Also remove temp directory if empty
                temp_dir = os.path.dirname(file_path)
                try:
                    os.rmdir(temp_dir)
                except OSError:
                    pass  # Directory not empty or other issue
        except Exception as e:
            logger.warning(f"Failed to clean up temp file {file_path}: {str(e)}")