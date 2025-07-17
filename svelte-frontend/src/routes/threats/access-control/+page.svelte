<script>
	import { onMount } from 'svelte';
	
	let threats = [];
	let threatStats = {
		total_threats: 0,
		active_threats: 0,
		investigating: 0,
		resolved: 0,
		false_positives: 0
	};
	let loading = true;
	let selectedThreat = null;
	let showThreatModal = false;
	let statusFilter = 'all';
	
	// Status update
	let updatingStatus = false;
	let statusUpdateForm = {
		status: '',
		investigation_notes: ''
	};
	
	onMount(async () => {
		await loadThreats();
		await loadThreatStats();
	});
	
	async function loadThreats() {
		try {
			loading = true;
			const url = statusFilter === 'all' 
				? 'http://localhost:8001/api/v1/threats/access-control'
				: `http://localhost:8001/api/v1/threats/access-control?status=${statusFilter}`;
			
			const response = await fetch(url);
			if (response.ok) {
				threats = await response.json();
			} else {
				console.error('Failed to load threats');
				threats = [];
			}
		} catch (error) {
			console.error('Error loading threats:', error);
			threats = [];
		} finally {
			loading = false;
		}
	}
	
	async function loadThreatStats() {
		try {
			const response = await fetch('http://localhost:8001/api/v1/threats/stats');
			if (response.ok) {
				threatStats = await response.json();
			}
		} catch (error) {
			console.error('Error loading threat stats:', error);
		}
	}
	
	async function viewThreatDetails(threat) {
		try {
			const response = await fetch(`http://localhost:8001/api/v1/threats/access-control/${threat.correlation_id}`);
			if (response.ok) {
				selectedThreat = await response.json();
				statusUpdateForm.status = selectedThreat.status;
				statusUpdateForm.investigation_notes = selectedThreat.investigation_notes || '';
				showThreatModal = true;
			}
		} catch (error) {
			console.error('Error loading threat details:', error);
		}
	}
	
	async function updateThreatStatus() {
		if (!selectedThreat) return;
		
		try {
			updatingStatus = true;
			const response = await fetch(`http://localhost:8001/api/v1/threats/access-control/${selectedThreat.correlation_id}/status`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(statusUpdateForm)
			});
			
			if (response.ok) {
				// Update local threat status
				selectedThreat.status = statusUpdateForm.status;
				selectedThreat.investigation_notes = statusUpdateForm.investigation_notes;
				
				// Refresh threats list and stats
				await loadThreats();
				await loadThreatStats();
				
				alert('Threat status updated successfully!');
			} else {
				throw new Error('Failed to update status');
			}
		} catch (error) {
			console.error('Error updating threat status:', error);
			alert('Failed to update threat status: ' + error.message);
		} finally {
			updatingStatus = false;
		}
	}
	
	function closeThreatModal() {
		showThreatModal = false;
		selectedThreat = null;
	}
	
	function getStatusColor(status) {
		switch (status) {
			case 'active': return 'bg-red-100 text-red-800';
			case 'investigating': return 'bg-yellow-100 text-yellow-800';
			case 'resolved': return 'bg-green-100 text-green-800';
			case 'false_positive': return 'bg-gray-100 text-gray-800';
			default: return 'bg-blue-100 text-blue-800';
		}
	}
	
	function getRiskColor(riskLevel) {
		switch (riskLevel?.toLowerCase()) {
			case 'critical': return 'bg-red-100 text-red-800 border-red-200';
			case 'high': return 'bg-orange-100 text-orange-800 border-orange-200';
			case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
			case 'low': return 'bg-green-100 text-green-800 border-green-200';
			default: return 'bg-gray-100 text-gray-800 border-gray-200';
		}
	}
	
	function formatDateTime(dateString) {
		return new Date(dateString).toLocaleString();
	}
	
	function formatBadgeIds(correlatedBadgeEvents) {
		if (!correlatedBadgeEvents || correlatedBadgeEvents.length === 0) {
			return {
				display: 'No badges',
				class: 'text-gray-400 italic'
			};
		}
		
		const badgeIds = correlatedBadgeEvents.map(event => event.badge_id);
		const uniqueBadgeIds = [...new Set(badgeIds)];
		
		if (uniqueBadgeIds.length === 1) {
			return {
				display: uniqueBadgeIds[0],
				class: 'text-gray-900 font-medium'
			};
		} else {
			return {
				display: `${uniqueBadgeIds.length} badges`,
				class: 'text-blue-600 font-medium',
				tooltip: uniqueBadgeIds.join(', ')
			};
		}
	}
	
	// Filter change handler
	async function handleFilterChange() {
		await loadThreats();
	}
	
	// Clear all threat correlations
	let clearingThreats = false;
	async function clearAllThreats() {
		if (!confirm('Are you sure you want to clear all threat correlations? This action cannot be undone.')) {
			return;
		}
		
		try {
			clearingThreats = true;
			const response = await fetch('http://localhost:8001/api/v1/threats/clear-all', {
				method: 'DELETE'
			});
			
			if (response.ok) {
				// Refresh threats list and stats
				await loadThreats();
				await loadThreatStats();
				alert('All threat correlations cleared successfully!');
			} else {
				throw new Error('Failed to clear threat correlations');
			}
		} catch (error) {
			console.error('Error clearing threats:', error);
			alert('Failed to clear threat correlations: ' + error.message);
		} finally {
			clearingThreats = false;
		}
	}
</script>

<svelte:head>
	<title>Potential Access Control Threats - SOP Agent</title>
</svelte:head>

<div class="space-y-6">
	<!-- Page Header -->
	<div class="flex justify-between items-start">
		<div>
			<h1 class="text-3xl font-bold text-gray-900">🚨 Potential Access Control Threats</h1>
			<p class="text-gray-600 mt-1">
				AI-powered correlation analysis of tailgating incidents and badge access patterns
			</p>
		</div>
		
		<div class="flex gap-2">
			<button 
				class="btn-secondary"
				on:click={() => { loadThreats(); loadThreatStats(); }}
			>
				🔄 Refresh
			</button>
			
			<button 
				class="btn-danger"
				on:click={clearAllThreats}
				disabled={clearingThreats || threats.length === 0}
			>
				{#if clearingThreats}
					🗑️ Clearing...
				{:else}
					🗑️ Clear All
				{/if}
			</button>
		</div>
	</div>
	
	<!-- Threat Statistics -->
	<div class="grid grid-cols-1 md:grid-cols-5 gap-4">
		<div class="card text-center">
			<h3 class="text-2xl font-bold text-blue-600">{threatStats.total_threats}</h3>
			<p class="text-sm text-gray-600">Total Threats</p>
		</div>
		
		<div class="card text-center">
			<h3 class="text-2xl font-bold text-red-600">{threatStats.active_threats}</h3>
			<p class="text-sm text-gray-600">Active</p>
		</div>
		
		<div class="card text-center">
			<h3 class="text-2xl font-bold text-yellow-600">{threatStats.investigating}</h3>
			<p class="text-sm text-gray-600">Investigating</p>
		</div>
		
		<div class="card text-center">
			<h3 class="text-2xl font-bold text-green-600">{threatStats.resolved}</h3>
			<p class="text-sm text-gray-600">Resolved</p>
		</div>
		
		<div class="card text-center">
			<h3 class="text-2xl font-bold text-gray-600">{threatStats.false_positives}</h3>
			<p class="text-sm text-gray-600">False Positives</p>
		</div>
	</div>
	
	<!-- Filter Controls -->
	<div class="card">
		<div class="flex items-center gap-4">
			<label class="font-medium text-gray-700">Filter by Status:</label>
			<select 
				bind:value={statusFilter}
				on:change={handleFilterChange}
				class="input-field max-w-xs"
			>
				<option value="all">All Threats</option>
				<option value="active">Active</option>
				<option value="investigating">Investigating</option>
				<option value="resolved">Resolved</option>
				<option value="false_positive">False Positives</option>
			</select>
		</div>
	</div>
	
	<!-- Threats List -->
	<div class="card">
		<h2 class="text-xl font-semibold text-gray-900 mb-4">Threat Correlations</h2>
		
		{#if loading}
			<div class="text-center py-8">
				<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-sop-primary mx-auto"></div>
				<p class="text-gray-500 mt-2">Loading threats...</p>
			</div>
		{:else if threats.length === 0}
			<div class="text-center py-8">
				<p class="text-gray-500">No threats found.</p>
				<p class="text-sm text-gray-400 mt-2">
					Process a tailgating event in the Event Simulator to generate correlations.
				</p>
			</div>
		{:else}
			<div class="overflow-x-auto">
				<table class="min-w-full divide-y divide-gray-200">
					<thead class="bg-gray-50">
						<tr>
							<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
								Threat ID
							</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
								Risk Level
							</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
								Confidence
							</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
								Badge ID(s)
							</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
								Status
							</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
								Created
							</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
								Actions
							</th>
						</tr>
					</thead>
					<tbody class="bg-white divide-y divide-gray-200">
						{#each threats as threat}
							<tr class="hover:bg-gray-50">
								<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
									{threat.correlation_id.substring(0, 8)}...
								</td>
								<td class="px-6 py-4 whitespace-nowrap">
									<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border {getRiskColor(threat.risk_level)}">
										{threat.risk_level}
									</span>
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
									{(threat.confidence_score * 100).toFixed(1)}%
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm">
									{#if formatBadgeIds(threat.correlated_badge_events).tooltip}
										<span 
											class="{formatBadgeIds(threat.correlated_badge_events).class}"
											title="{formatBadgeIds(threat.correlated_badge_events).tooltip}"
										>
											{formatBadgeIds(threat.correlated_badge_events).display}
										</span>
									{:else}
										<span class="{formatBadgeIds(threat.correlated_badge_events).class}">
											{formatBadgeIds(threat.correlated_badge_events).display}
										</span>
									{/if}
								</td>
								<td class="px-6 py-4 whitespace-nowrap">
									<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {getStatusColor(threat.status)}">
										{threat.status.replace('_', ' ')}
									</span>
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
									{formatDateTime(threat.created_at)}
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
									<button 
										class="text-sop-primary hover:text-sop-primary-dark"
										on:click={() => viewThreatDetails(threat)}
									>
										View Details
									</button>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{/if}
	</div>
</div>

<!-- Threat Details Modal -->
{#if showThreatModal && selectedThreat}
	<div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
		<div class="relative top-20 mx-auto p-5 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white">
			<!-- Modal Header -->
			<div class="flex justify-between items-start mb-4">
				<div>
					<h3 class="text-lg font-semibold text-gray-900">
						Threat Correlation Details
					</h3>
					<p class="text-sm text-gray-500">ID: {selectedThreat.correlation_id}</p>
				</div>
				<button 
					class="text-gray-400 hover:text-gray-600"
					on:click={closeThreatModal}
				>
					<span class="text-2xl">&times;</span>
				</button>
			</div>
			
			<!-- Modal Content -->
			<div class="space-y-6">
				<!-- Risk Assessment -->
				<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
					<div class="text-center">
						<span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border {getRiskColor(selectedThreat.risk_level)}">
							{selectedThreat.risk_level} Risk
						</span>
					</div>
					<div class="text-center">
						<span class="text-lg font-semibold">{(selectedThreat.confidence_score * 100).toFixed(1)}%</span>
						<p class="text-sm text-gray-500">Confidence</p>
					</div>
					<div class="text-center">
						<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {getStatusColor(selectedThreat.status)}">
							{selectedThreat.status.replace('_', ' ')}
						</span>
					</div>
				</div>
				
				<!-- Analysis Summary -->
				<div>
					<h4 class="font-medium text-gray-900 mb-2">Analysis Summary</h4>
					<div class="bg-gray-50 rounded-lg p-4">
						<p class="text-gray-700">{selectedThreat.analysis_summary}</p>
					</div>
				</div>
				
				<!-- Correlated Events -->
				{#if selectedThreat.correlated_badge_events && selectedThreat.correlated_badge_events.length > 0}
					<div>
						<h4 class="font-medium text-gray-900 mb-2">Correlated Badge Events</h4>
						<div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
							{#each selectedThreat.correlated_badge_events as badgeEvent}
								<div class="flex justify-between items-center py-2 border-b border-blue-200 last:border-b-0">
									<div>
										<span class="font-medium">{badgeEvent.employee_name}</span>
										<span class="text-sm text-gray-600">({badgeEvent.badge_id})</span>
									</div>
									<div class="text-right">
										<div class="text-sm">{badgeEvent.department}</div>
										<div class="text-xs text-gray-500">{badgeEvent.time_difference_seconds}s before</div>
									</div>
								</div>
							{/each}
						</div>
					</div>
				{/if}
				
				<!-- AI Agent Analysis -->
				{#if selectedThreat.agent_analysis}
					<div>
						<h4 class="font-medium text-gray-900 mb-2">AI Agent Analysis</h4>
						<div class="bg-green-50 border border-green-200 rounded-lg p-4">
							<pre class="text-sm text-gray-700 whitespace-pre-wrap">{JSON.stringify(selectedThreat.agent_analysis, null, 2)}</pre>
						</div>
					</div>
				{/if}
				
				<!-- Status Update Form -->
				<div class="border-t pt-4">
					<h4 class="font-medium text-gray-900 mb-4">Update Investigation Status</h4>
					<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
							<select bind:value={statusUpdateForm.status} class="input-field">
								<option value="active">Active</option>
								<option value="investigating">Investigating</option>
								<option value="resolved">Resolved</option>
								<option value="false_positive">False Positive</option>
							</select>
						</div>
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-2">Investigation Notes</label>
							<textarea 
								bind:value={statusUpdateForm.investigation_notes}
								class="input-field h-24"
								placeholder="Add investigation notes..."
							></textarea>
						</div>
					</div>
					
					<div class="flex justify-end gap-3 mt-4">
						<button 
							class="btn-secondary"
							on:click={closeThreatModal}
						>
							Cancel
						</button>
						<button 
							class="btn-primary"
							on:click={updateThreatStatus}
							disabled={updatingStatus}
						>
							{#if updatingStatus}
								Updating...
							{:else}
								Update Status
							{/if}
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
{/if}