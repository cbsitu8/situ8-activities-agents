import mammoth
import os
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

class DocumentReader:
    """Extract text content from .docx and .md files"""
    
    def __init__(self):
        self.supported_extensions = ['.docx', '.md']
        self.max_file_size = 2 * 1024 * 1024  # 2MB in bytes
    
    def is_supported_file(self, filename: str) -> bool:
        """Check if file type is supported"""
        _, ext = os.path.splitext(filename.lower())
        return ext in self.supported_extensions
    
    def validate_file_size(self, file_path: str) -> bool:
        """Validate file size is within limits"""
        try:
            file_size = os.path.getsize(file_path)
            return file_size <= self.max_file_size
        except OSError as e:
            logger.error(f"Error checking file size for {file_path}: {str(e)}")
            return False
    
    def extract_text(self, file_path: str) -> Tuple[str, Optional[str]]:
        """
        Extract text content from supported file types
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Tuple of (extracted_text, error_message)
            If successful: (text_content, None)
            If failed: ("", error_message)
        """
        try:
            # Validate file exists
            if not os.path.exists(file_path):
                return "", f"File not found: {file_path}"
            
            # Validate file size
            if not self.validate_file_size(file_path):
                file_size = os.path.getsize(file_path)
                return "", f"File size {file_size} bytes exceeds maximum allowed size of {self.max_file_size} bytes"
            
            # Get file extension
            _, ext = os.path.splitext(file_path.lower())
            
            if not self.is_supported_file(file_path):
                return "", f"Unsupported file type: {ext}. Supported types: {', '.join(self.supported_extensions)}"
            
            # Process based on file type
            if ext == '.docx':
                return self._extract_from_docx(file_path)
            elif ext == '.md':
                return self._extract_from_markdown(file_path)
            else:
                return "", f"Unsupported file extension: {ext}"
                
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {str(e)}")
            return "", f"Error processing file: {str(e)}"
    
    def _extract_from_docx(self, file_path: str) -> Tuple[str, Optional[str]]:
        """Extract text from .docx file using mammoth"""
        try:
            with open(file_path, "rb") as docx_file:
                # Use mammoth to extract text
                result = mammoth.extract_raw_text(docx_file)
                
                # Check for warnings
                if result.messages:
                    warnings = [msg.message for msg in result.messages]
                    logger.warning(f"Mammoth warnings for {file_path}: {warnings}")
                
                # Clean up the text
                text = result.value.strip()
                
                if not text:
                    return "", "Document appears to be empty or contains no extractable text"
                
                logger.info(f"Successfully extracted {len(text)} characters from {file_path}")
                return text, None
                
        except Exception as e:
            logger.error(f"Error extracting from .docx file {file_path}: {str(e)}")
            return "", f"Error reading .docx file: {str(e)}"
    
    def _extract_from_markdown(self, file_path: str) -> Tuple[str, Optional[str]]:
        """Extract text from .md file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as md_file:
                text = md_file.read().strip()
                
                if not text:
                    return "", "Markdown file appears to be empty"
                
                logger.info(f"Successfully extracted {len(text)} characters from {file_path}")
                return text, None
                
        except UnicodeDecodeError as e:
            logger.error(f"Encoding error reading {file_path}: {str(e)}")
            return "", f"Unable to read file - encoding error: {str(e)}"
        except Exception as e:
            logger.error(f"Error extracting from .md file {file_path}: {str(e)}")
            return "", f"Error reading .md file: {str(e)}"
    
    def get_file_info(self, file_path: str) -> dict:
        """Get basic file information"""
        try:
            stat = os.stat(file_path)
            _, ext = os.path.splitext(file_path.lower())
            
            return {
                "filename": os.path.basename(file_path),
                "file_size": stat.st_size,
                "file_type": ext,
                "is_supported": self.is_supported_file(file_path),
                "size_valid": self.validate_file_size(file_path)
            }
        except Exception as e:
            logger.error(f"Error getting file info for {file_path}: {str(e)}")
            return {
                "filename": os.path.basename(file_path),
                "error": str(e)
            }