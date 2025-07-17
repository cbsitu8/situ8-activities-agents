<script>
	import { createEventDispatcher } from 'svelte';
	
	export let sops;
	export let selectedSOP = null;
	
	const dispatch = createEventDispatcher();
	
	function selectSOP(sop) {
		selectedSOP = sop;
		dispatch('selected', sop);
	}
	
	async function deleteSOP(sop) {
		if (!confirm(`Are you sure you want to delete "${sop.name}"?`)) {
			return;
		}
		
		try {
			const response = await fetch(`http://localhost:8001/api/v1/sops/${sop.id}`, {
				method: 'DELETE'
			});
			
			if (!response.ok) {
				throw new Error('Failed to delete SOP');
			}
			
			dispatch('deleted', { sopId: sop.id });
		} catch (err) {
			alert('Failed to delete SOP: ' + (err instanceof Error ? err.message : 'Unknown error'));
		}
	}
	
	function getStatusColor(status) {
		switch (status) {
			case 'completed': return 'bg-green-100 text-green-800';
			case 'processing': return 'bg-yellow-100 text-yellow-800';
			case 'error': return 'bg-red-100 text-red-800';
			default: return 'bg-gray-100 text-gray-800';
		}
	}
	
	function formatDate(dateString) {
		return new Date(dateString).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'short',
			day: 'numeric',
			hour: '2-digit',
			minute: '2-digit'
		});
	}
</script>

{#if sops.length === 0}
	<div class="text-center py-8 border-2 border-dashed border-gray-300 rounded-lg">
		<div class="text-4xl mb-4">📄</div>
		<h3 class="text-lg font-medium text-gray-900 mb-2">No SOPs Found</h3>
		<p class="text-gray-500">Upload your first SOP document to get started.</p>
	</div>
{:else}
	<div class="space-y-3">
		{#each sops as sop}
			<div class="border rounded-lg p-4 transition-colors hover:bg-gray-50 border-gray-200">
				<div class="flex items-start justify-between">
					<div class="flex-1 min-w-0">
						<div class="flex items-center space-x-2 mb-2">
							<h3 class="text-lg font-medium text-gray-900 truncate">
								{sop.name}
							</h3>
							<span class="px-2 py-1 text-xs font-medium rounded-full {getStatusColor(sop.upload_status)}">
								{sop.upload_status}
							</span>
						</div>
						
						<div class="grid grid-cols-2 gap-4 text-sm text-gray-600">
							<div>
								<span class="font-medium">File Type:</span>
								<span class="ml-1 uppercase">{sop.file_type || 'unknown'}</span>
							</div>
							<div>
								<span class="font-medium">Rules:</span>
								<span class="ml-1">{sop.rule_count || 0}</span>
							</div>
							<div class="col-span-2">
								<span class="font-medium">Created:</span>
								<span class="ml-1">{formatDate(sop.created_at)}</span>
							</div>
						</div>
					</div>
					
					<div class="flex items-center space-x-2 ml-4">
						<button
							class="btn-secondary text-sm py-1 px-3"
							on:click={() => selectSOP(sop)}
							title="View Rules"
						>
							🔍 View Rules
						</button>
						
						<button
							class="text-red-500 hover:text-red-700 p-1"
							on:click={() => deleteSOP(sop)}
							title="Delete SOP"
						>
							🗑️
						</button>
					</div>
				</div>
				
				{#if sop.upload_status === 'error'}
					<div class="mt-2 text-sm text-red-600">
						⚠️ Processing failed. Please try uploading again.
					</div>
				{/if}
			</div>
		{/each}
	</div>
{/if}