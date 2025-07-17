<script>
	import { onMount } from 'svelte';
	
	export let sop;
	
	let rules = [];
	let loading = false;
	let error = '';
	
	$: if (sop) {
		loadRules();
	}
	
	async function loadRules() {
		try {
			loading = true;
			error = '';
			
			const response = await fetch(`http://localhost:8001/api/v1/sops/${sop.id}/rules`);
			if (!response.ok) {
				throw new Error('Failed to load rules');
			}
			
			const data = await response.json();
			rules = data.rules || [];
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to load rules';
		} finally {
			loading = false;
		}
	}
	
	function getPriorityColor(priority) {
		switch (priority.toUpperCase()) {
			case 'CRITICAL': return 'priority-critical';
			case 'HIGH': return 'priority-high';
			case 'MEDIUM': return 'priority-medium';
			case 'LOW': return 'priority-low';
			default: return 'priority-medium';
		}
	}
	
	function getRuleTypeIcon(ruleType) {
		switch (ruleType) {
			case 'exact': return '🎯';
			case 'keyword': return '🔍';
			case 'pattern': return '🔄';
			case 'semantic': return '🧠';
			default: return '📝';
		}
	}
	
	function formatRuleValue(ruleValue) {
		if (Array.isArray(ruleValue)) {
			return ruleValue.join(', ');
		}
		return String(ruleValue);
	}
</script>

<div class="space-y-4">
	<!-- SOP Header -->
	<div class="border-b border-gray-200 pb-4">
		<h3 class="text-lg font-semibold text-gray-900">{sop.name}</h3>
		<div class="grid grid-cols-2 gap-4 mt-2 text-sm text-gray-600">
			<div>
				<span class="font-medium">File Type:</span>
				<span class="ml-1 uppercase">{sop.file_type}</span>
			</div>
			<div>
				<span class="font-medium">Status:</span>
				<span class="ml-1 capitalize">{sop.upload_status}</span>
			</div>
		</div>
	</div>
	
	<!-- Rules Section -->
	{#if loading}
		<div class="text-center py-8">
			<div class="animate-spin text-2xl mb-2">⟳</div>
			<p class="text-gray-500">Loading rules...</p>
		</div>
	{:else if error}
		<div class="bg-red-50 border border-red-200 rounded-lg p-4">
			<div class="flex items-center">
				<span class="text-red-500 mr-2">⚠️</span>
				<span class="text-red-700">{error}</span>
			</div>
		</div>
	{:else if rules.length === 0}
		<div class="text-center py-8 border-2 border-dashed border-gray-300 rounded-lg">
			<div class="text-3xl mb-2">📋</div>
			<p class="text-gray-500">No rules extracted from this SOP</p>
		</div>
	{:else}
		<div class="space-y-4">
			<div class="flex justify-between items-center">
				<h4 class="font-medium text-gray-900">Extracted Rules ({rules.length})</h4>
				<div class="text-sm text-gray-500">
					Auto-generated from SOP content
				</div>
			</div>
			
			{#each rules as rule, index}
				<div class="border border-gray-200 rounded-lg p-4">
					<div class="flex items-start justify-between mb-3">
						<div class="flex items-center space-x-2">
							<span class="text-lg">{getRuleTypeIcon(rule.rule_type)}</span>
							<span class="font-medium text-gray-900 capitalize">
								{rule.rule_type} Match
							</span>
							<span class="px-2 py-1 text-xs font-medium rounded-full {getPriorityColor(rule.priority)}">
								{rule.priority}
							</span>
						</div>
						<div class="text-xs text-gray-500">
							Rule #{index + 1}
						</div>
					</div>
					
					<!-- Rule Values -->
					<div class="mb-3">
						<h5 class="text-sm font-medium text-gray-700 mb-1">Match Criteria:</h5>
						<div class="bg-gray-50 rounded p-2 text-sm">
							{formatRuleValue(rule.rule_value)}
						</div>
					</div>
					
					<!-- Agent Assignments -->
					{#if rule.agent_assignments && rule.agent_assignments.length > 0}
						<div class="mb-3">
							<h5 class="text-sm font-medium text-gray-700 mb-1">Assigned User Groups:</h5>
							<div class="flex flex-wrap gap-2">
								{#each rule.agent_assignments as agent}
									<span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
										{agent}
									</span>
								{/each}
							</div>
						</div>
					{/if}
					
					<!-- Rule Metadata -->
					<div class="text-xs text-gray-500 border-t border-gray-100 pt-2">
						Created: {new Date(rule.created_at).toLocaleString()}
					</div>
				</div>
			{/each}
		</div>
	{/if}
	
	<!-- Rule Type Legend -->
	<div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
		<h5 class="font-medium text-gray-900 mb-2">Rule Types</h5>
		<div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
			<div class="flex items-center space-x-2">
				<span>🎯</span>
				<span><strong>Exact:</strong> Direct event name matches</span>
			</div>
			<div class="flex items-center space-x-2">
				<span>🔍</span>
				<span><strong>Keyword:</strong> Key term detection</span>
			</div>
			<div class="flex items-center space-x-2">
				<span>🔄</span>
				<span><strong>Pattern:</strong> Regex pattern matching</span>
			</div>
			<div class="flex items-center space-x-2">
				<span>🧠</span>
				<span><strong>Semantic:</strong> AI similarity matching</span>
			</div>
		</div>
	</div>
</div>