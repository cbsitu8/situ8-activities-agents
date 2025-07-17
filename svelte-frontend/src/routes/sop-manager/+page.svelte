<script>
	import { onMount } from 'svelte';
	import SOPUploader from '$lib/components/SOPUploader.svelte';
	import SOPList from '$lib/components/SOPList.svelte';
	import RuleViewer from '$lib/components/RuleViewer.svelte';
	
	let sops = [];
	let selectedSOP = null;
	let showRulesModal = false;
	let loading = false;
	let error = '';
	
	onMount(async () => {
		await loadSOPs();
	});
	
	async function loadSOPs() {
		try {
			loading = true;
			error = '';
			
			const response = await fetch('http://localhost:8001/api/v1/sops');
			if (!response.ok) {
				throw new Error(`Failed to load SOPs: ${response.statusText}`);
			}
			
			const data = await response.json();
			sops = data.sops || [];
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to load SOPs';
			console.error('Error loading SOPs:', err);
		} finally {
			loading = false;
		}
	}
	
	function handleSOPUploaded(event) {
		// Refresh the SOP list after successful upload
		loadSOPs();
		
		// Show success message
		const { detail } = event;
		if (detail.total) {
			// Bulk upload result
			console.log(`Bulk upload completed: ${detail.successful}/${detail.total} files processed successfully`);
			if (detail.errors && detail.errors.length > 0) {
				console.log('Upload errors:', detail.errors);
			}
		} else {
			// Single upload result
			console.log('SOP uploaded successfully:', detail);
		}
	}
	
	function handleSOPSelected(event) {
		selectedSOP = event.detail;
		showRulesModal = true;
	}

	function closeRulesModal() {
		showRulesModal = false;
		selectedSOP = null;
	}
	
	function handleSOPDeleted(event) {
		// Refresh the list and clear selection
		loadSOPs();
		if (selectedSOP && selectedSOP.id === event.detail.sopId) {
			selectedSOP = null;
		}
	}
</script>

<svelte:head>
	<title>SOP Manager - SOP Agent</title>
</svelte:head>

<div class="space-y-6">
	<!-- Page Header -->
	<div class="flex justify-between items-center">
		<div>
			<h1 class="text-3xl font-bold text-gray-900">📄 SOP Manager</h1>
			<p class="text-gray-600 mt-1">
				Upload and manage Standard Operating Procedures for intelligent event routing
			</p>
		</div>
		
		<div class="flex items-center space-x-4">
			<button 
				class="btn-secondary"
				on:click={loadSOPs}
				disabled={loading}
			>
				{#if loading}
					<span class="animate-spin">⟳</span> Loading...
				{:else}
					🔄 Refresh
				{/if}
			</button>
		</div>
	</div>
	
	<!-- Error Display -->
	{#if error}
		<div class="bg-red-50 border border-red-200 rounded-lg p-4">
			<div class="flex items-center">
				<span class="text-red-500 mr-2">⚠️</span>
				<span class="text-red-700">{error}</span>
			</div>
		</div>
	{/if}
	
	<!-- Main Content -->
	<div class="space-y-6">
		<!-- SOP Uploader -->
		<div class="card">
			<h2 class="text-xl font-semibold text-gray-900 mb-4">📤 Upload SOP Document</h2>
			<SOPUploader on:uploaded={handleSOPUploaded} />
		</div>
		
		<!-- SOP List -->
		<div class="card">
			<h2 class="text-xl font-semibold text-gray-900 mb-4">
				📋 SOP Documents
				{#if sops.length > 0}
					<span class="text-sm font-normal text-gray-500">({sops.length} documents)</span>
				{/if}
			</h2>
			
			{#if loading}
				<div class="text-center py-8">
					<div class="animate-spin text-3xl mb-2">⟳</div>
					<p class="text-gray-500">Loading SOPs...</p>
				</div>
			{:else}
				<SOPList 
					{sops} 
					selectedSOP={null}
					on:selected={handleSOPSelected}
					on:deleted={handleSOPDeleted}
				/>
			{/if}
		</div>
	</div>

	<!-- Rules Modal -->
	{#if showRulesModal && selectedSOP}
		<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
			<div class="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
				<!-- Modal Header -->
				<div class="flex items-center justify-between p-6 border-b border-gray-200">
					<h2 class="text-2xl font-semibold text-gray-900">🔍 Rule Details</h2>
					<button 
						class="text-gray-400 hover:text-gray-600 text-2xl font-bold"
						on:click={closeRulesModal}
					>
						×
					</button>
				</div>
				
				<!-- Modal Content -->
				<div class="p-6 overflow-y-auto max-h-[calc(90vh-8rem)]">
					<RuleViewer sop={selectedSOP} />
				</div>
				
				<!-- Modal Footer -->
				<div class="flex justify-end p-6 border-t border-gray-200">
					<button 
						class="btn-secondary"
						on:click={closeRulesModal}
					>
						Close
					</button>
				</div>
			</div>
		</div>
	{/if}
	
	<!-- Statistics Footer -->
	<div class="bg-white rounded-lg shadow-md p-6">
		<h3 class="text-lg font-semibold text-gray-900 mb-4">📊 SOP Statistics</h3>
		<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
			<div class="text-center">
				<div class="text-2xl font-bold text-sop-primary">{sops.length}</div>
				<div class="text-sm text-gray-500">Total SOPs</div>
			</div>
			<div class="text-center">
				<div class="text-2xl font-bold text-sop-success">
					{sops.reduce((sum, sop) => sum + (sop.rule_count || 0), 0)}
				</div>
				<div class="text-sm text-gray-500">Total Rules</div>
			</div>
			<div class="text-center">
				<div class="text-2xl font-bold text-sop-warning">
					{sops.filter(sop => sop.upload_status === 'completed').length}
				</div>
				<div class="text-sm text-gray-500">Processed</div>
			</div>
			<div class="text-center">
				<div class="text-2xl font-bold text-sop-secondary">
					{sops.filter(sop => sop.upload_status === 'pending').length}
				</div>
				<div class="text-sm text-gray-500">Pending</div>
			</div>
		</div>
	</div>
</div>