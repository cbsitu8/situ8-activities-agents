<script>
	import { createEventDispatcher } from 'svelte';
	
	const dispatch = createEventDispatcher();
	
	let fileInput;
	let dragActive = false;
	let uploading = false;
	let uploadProgress = '';
	let error = '';
	let selectedFiles = [];
	
	const acceptedTypes = ['.docx', '.md', '.txt'];
	
	function handleDragOver(event) {
		event.preventDefault();
		dragActive = true;
	}
	
	function handleDragLeave(event) {
		event.preventDefault();
		dragActive = false;
	}
	
	function handleDrop(event) {
		event.preventDefault();
		dragActive = false;
		
		const files = event.dataTransfer?.files;
		if (files && files.length > 0) {
			handleMultipleFiles(Array.from(files));
		}
	}
	
	function handleInputChange(event) {
		const target = event.target;
		const files = target.files;
		if (files && files.length > 0) {
			handleMultipleFiles(Array.from(files));
		}
	}
	
	function handleMultipleFiles(files) {
		selectedFiles = [];
		error = '';
		
		// Validate each file
		for (const file of files) {
			const extension = '.' + file.name.split('.').pop()?.toLowerCase();
			if (!acceptedTypes.includes(extension)) {
				error = `Unsupported file type in ${file.name}. Please use: ${acceptedTypes.join(', ')}`;
				return;
			}
			
			if (file.size > 10 * 1024 * 1024) {
				error = `File ${file.name} is too large. Maximum size is 10MB.`;
				return;
			}
		}
		
		if (files.length > 10) {
			error = 'Maximum 10 files allowed per upload.';
			return;
		}
		
		selectedFiles = files;
		
		// If only one file, upload immediately
		if (files.length === 1) {
			uploadFile(files[0]);
		}
	}
	
	
	async function uploadSelectedFiles() {
		if (selectedFiles.length === 0) {
			error = 'No files selected.';
			return;
		}
		
		await uploadBulkFiles(selectedFiles);
	}
	
	function removeFile(index) {
		selectedFiles = selectedFiles.filter((_, i) => i !== index);
	}
	
	function clearSelection() {
		selectedFiles = [];
		if (fileInput) fileInput.value = '';
		error = '';
	}
	
	async function uploadFile(file) {
		try {
			uploading = true;
			error = '';
			uploadProgress = 'Uploading file...';
			
			const formData = new FormData();
			formData.append('file', file);
			formData.append('name', file.name);
			
			uploadProgress = 'Processing document...';
			
			const response = await fetch('http://localhost:8001/api/v1/sop/process', {
				method: 'POST',
				body: formData
			});
			
			if (!response.ok) {
				const errorData = await response.json().catch(() => ({}));
				throw new Error(errorData.detail || `Upload failed: ${response.statusText}`);
			}
			
			uploadProgress = 'Extracting rules...';
			
			const result = await response.json();
			
			uploadProgress = 'Generating embeddings...';
			
			// Small delay to show progress
			await new Promise(resolve => setTimeout(resolve, 500));
			
			uploadProgress = 'Complete!';
			
			// Dispatch success event
			dispatch('uploaded', {
				sopId: result.sop_id,
				name: result.name,
				rulesExtracted: result.rules_extracted
			});
			
			// Reset form
			if (fileInput) fileInput.value = '';
			
			// Clear progress after delay
			setTimeout(() => {
				uploadProgress = '';
				uploading = false;
			}, 2000);
			
		} catch (err) {
			error = err instanceof Error ? err.message : 'Upload failed';
			uploading = false;
			uploadProgress = '';
		}
	}
	
	async function uploadBulkFiles(files) {
		try {
			uploading = true;
			error = '';
			uploadProgress = 'Uploading files...';
			
			const formData = new FormData();
			for (const file of files) {
				formData.append('files', file);
			}
			
			uploadProgress = 'Processing documents...';
			
			const response = await fetch('http://localhost:8001/api/v1/sop/process-bulk', {
				method: 'POST',
				body: formData
			});
			
			if (!response.ok) {
				const errorData = await response.json().catch(() => ({}));
				throw new Error(errorData.detail || `Upload failed: ${response.statusText}`);
			}
			
			uploadProgress = 'Extracting rules...';
			
			const result = await response.json();
			
			uploadProgress = 'Complete!';
			
			// Dispatch success event
			dispatch('uploaded', {
				total: result.total_files,
				successful: result.successful,
				failed: result.failed,
				results: result.results,
				errors: result.errors
			});
			
			// Reset form
			selectedFiles = [];
			if (fileInput) fileInput.value = '';
			
			// Clear progress after delay
			setTimeout(() => {
				uploadProgress = '';
				uploading = false;
			}, 2000);
			
		} catch (err) {
			error = err instanceof Error ? err.message : 'Bulk upload failed';
			uploading = false;
			uploadProgress = '';
		}
	}
	
	function openFileDialog() {
		fileInput?.click();
	}
</script>

<div class="space-y-4">
	<!-- Clear Selection Button -->
	<div class="flex items-center justify-end mb-4">
		{#if selectedFiles.length > 0}
			<button 
				class="text-sm text-gray-500 hover:text-gray-700"
				on:click={clearSelection}
			>
				Clear Selection
			</button>
		{/if}
	</div>

	<!-- File Input (Hidden) -->
	<input
		bind:this={fileInput}
		type="file"
		accept=".docx,.md,.txt"
		multiple
		on:change={handleInputChange}
		class="hidden"
	/>
	
	<!-- Drag & Drop Area -->
	<div
		class="border-2 border-dashed rounded-lg p-8 text-center transition-colors
			{dragActive ? 'border-sop-primary bg-blue-50' : 'border-gray-300 hover:border-gray-400'}
			{uploading ? 'opacity-50 pointer-events-none' : 'cursor-pointer'}"
		on:dragover={handleDragOver}
		on:dragleave={handleDragLeave}
		on:drop={handleDrop}
		on:click={openFileDialog}
		role="button"
		tabindex="0"
		on:keydown={(e) => e.key === 'Enter' && openFileDialog()}
	>
		{#if uploading}
			<div class="space-y-3">
				<div class="text-4xl">⏳</div>
				<div class="text-lg font-medium text-gray-900">
					Processing SOPs...
				</div>
				<div class="text-sm text-gray-600">{uploadProgress}</div>
				<div class="w-full bg-gray-200 rounded-full h-2 max-w-md mx-auto">
					<div class="bg-sop-primary h-2 rounded-full animate-pulse" style="width: 70%"></div>
				</div>
			</div>
		{:else}
			<div class="space-y-3">
				<div class="text-4xl">📚</div>
				<div class="text-lg font-medium text-gray-900">
					Drop SOP documents here, or click to browse
				</div>
				<div class="text-sm text-gray-600">
					Supports: .docx, .md, .txt files (max 10MB each, up to 10 files)
				</div>
				<button type="button" class="btn-primary">
					Choose Files
				</button>
			</div>
		{/if}
	</div>

	<!-- Selected Files Display -->
	{#if selectedFiles.length > 1}
		<div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
			<h4 class="font-medium text-gray-900 mb-3">Selected Files ({selectedFiles.length})</h4>
			<div class="space-y-2 max-h-48 overflow-y-auto">
				{#each selectedFiles as file, index}
					<div class="flex items-center justify-between bg-white rounded p-2 border">
						<div class="flex items-center space-x-2 flex-1 min-w-0">
							<span class="text-lg">📄</span>
							<span class="text-sm text-gray-900 truncate">{file.name}</span>
							<span class="text-xs text-gray-500">
								({(file.size / 1024 / 1024).toFixed(1)}MB)
							</span>
						</div>
						<button 
							class="text-red-500 hover:text-red-700 p-1"
							on:click={() => removeFile(index)}
							title="Remove file"
						>
							✕
						</button>
					</div>
				{/each}
			</div>
			<div class="mt-4 flex justify-between items-center">
				<span class="text-sm text-gray-600">
					Total size: {(selectedFiles.reduce((sum, file) => sum + file.size, 0) / 1024 / 1024).toFixed(1)}MB
				</span>
				<button 
					class="btn-primary"
					on:click={uploadSelectedFiles}
					disabled={uploading}
				>
					Upload {selectedFiles.length} Files
				</button>
			</div>
		</div>
	{/if}
	
	<!-- Error Display -->
	{#if error}
		<div class="bg-red-50 border border-red-200 rounded-lg p-4">
			<div class="flex items-center">
				<span class="text-red-500 mr-2">⚠️</span>
				<span class="text-red-700">{error}</span>
				<button 
					class="ml-auto text-red-500 hover:text-red-700"
					on:click={() => error = ''}
				>
					✕
				</button>
			</div>
		</div>
	{/if}
	
</div>