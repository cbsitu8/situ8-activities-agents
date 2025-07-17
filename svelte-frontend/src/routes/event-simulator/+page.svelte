<script>
	import { onMount } from 'svelte';
	
	// Event Simulator with realistic mock data
	let selectedEvent = '';
	let isSequentialRunning = false;
	let isSimulating = false;
	let simulationResults = [];
	let showResults = false;
	let loadingResults = false;
	
	// Create realistic timestamps with overlapping times
	const now = new Date();
	const getTimestamp = (minutesAgo) => new Date(now.getTime() - minutesAgo * 60000);
	
	// Mock Computer Vision Events with creation_time
	const computerVisionMockData = [
		{
			event_type: 'Person Brandishing Firearm',
			creation_time: getTimestamp(45).toISOString(),
			location: 'Building A - Main Entrance',
			severity: 'Critical',
			confidence: 0.89,
			camera_id: 'CAM-001-ENTRANCE'
		},
		{
			event_type: 'Smoke or Fire',
			creation_time: getTimestamp(42).toISOString(),
			location: 'Building B - Kitchen Area',
			severity: 'High',
			confidence: 0.95,
			camera_id: 'CAM-015-KITCHEN'
		},
		{
			event_type: 'Person Jumping Fence',
			creation_time: getTimestamp(38).toISOString(),
			location: 'Perimeter - North Gate',
			severity: 'High',
			confidence: 0.82,
			camera_id: 'CAM-022-PERIMETER'
		},
		{
			event_type: 'Door Propped Open',
			creation_time: getTimestamp(35).toISOString(),
			location: 'Building A - Emergency Exit',
			severity: 'Medium',
			confidence: 0.76,
			camera_id: 'CAM-008-EXIT'
		},
		{
			event_type: 'Tailgating',
			creation_time: getTimestamp(30).toISOString(),
			location: 'Building C - Secure Zone Entry',
			severity: 'Medium',
			confidence: 0.71,
			camera_id: 'CAM-005-SECURE'
		},
		{
			event_type: 'Person Falling Down',
			creation_time: getTimestamp(25).toISOString(),
			location: 'Building A - Lobby',
			severity: 'High',
			confidence: 0.88,
			camera_id: 'CAM-003-LOBBY'
		}
	];
	
	// Mock Access Control Events with timestamp - Enhanced with Tailgating Correlations
	const accessControlMockData = [
		{
			event_type: 'Door Forced Open',
			timestamp: getTimestamp(47).toISOString(),
			location: 'Building A - Server Room',
			severity: 'Critical',
			badge_id: null,
			door_id: 'DOOR-A-SERVER',
			access_level_required: 'ADMIN'
		},
		{
			event_type: 'Invalid Badge Read',
			timestamp: getTimestamp(40).toISOString(),
			location: 'Building B - Executive Floor',
			severity: 'Medium',
			badge_id: 'BADGE-7829',
			door_id: 'DOOR-B-EXEC',
			access_level_required: 'EXECUTIVE'
		},
		{
			event_type: 'Door Held Open',
			timestamp: getTimestamp(36).toISOString(),
			location: 'Building C - Data Center',
			severity: 'Medium',
			badge_id: 'BADGE-4521',
			door_id: 'DOOR-C-DATA',
			access_level_required: 'TECH'
		},
		{
			event_type: 'Granted Access',
			timestamp: getTimestamp(32).toISOString(),
			location: 'Building A - Main Entrance',
			severity: 'Low',
			badge_id: 'BADGE-1234',
			door_id: 'DOOR-A-MAIN',
			access_level_required: 'EMPLOYEE'
		},
		{
			// CORRELATION EVENT: Badge access 3 seconds before tailgating at same location
			event_type: 'Granted Access',
			timestamp: getTimestamp(30.05).toISOString(), // 3 seconds before tailgating
			location: 'Building C - Secure Zone Entry',
			severity: 'Low',
			badge_id: 'BADGE-4521',
			door_id: 'DOOR-C-SECURE',
			access_level_required: 'MANAGER'
		},
		{
			event_type: 'Invalid Badge Read',
			timestamp: getTimestamp(28).toISOString(),
			location: 'Building A - Parking Garage',
			severity: 'Medium',
			badge_id: 'BADGE-9999',
			door_id: 'DOOR-A-GARAGE',
			access_level_required: 'EMPLOYEE'
		},
		{
			event_type: 'Door Forced Open',
			timestamp: getTimestamp(22).toISOString(),
			location: 'Building B - Storage Room',
			severity: 'High',
			badge_id: null,
			door_id: 'DOOR-B-STORAGE',
			access_level_required: 'EMPLOYEE'
		},
		{
			// CORRELATION EVENT: Multiple badge access at same location as upcoming tailgating
			event_type: 'Granted Access',
			timestamp: getTimestamp(20.5).toISOString(), // 30 seconds before Building C tailgating
			location: 'Building C - Secure Zone Entry',
			severity: 'Low',
			badge_id: 'BADGE-4521',
			door_id: 'DOOR-C-SECURE',
			access_level_required: 'MANAGER'
		},
		{
			// CORRELATION EVENT: Same badge used again (anti-passback pattern)
			event_type: 'Granted Access',
			timestamp: getTimestamp(19.8).toISOString(), // 12 seconds after first access
			location: 'Building C - Secure Zone Entry',
			severity: 'Low',
			badge_id: 'BADGE-4521',
			door_id: 'DOOR-C-SECURE',
			access_level_required: 'MANAGER'
		}
	];
	
	// Combine all event types for dropdown
	const allEventTypes = [
		...computerVisionMockData.map(e => ({ ...e, source: 'computer_vision' })),
		...accessControlMockData.map(e => ({ ...e, source: 'access_control' }))
	];
	
	// Extract unique event types for dropdown
	const allUniqueEvents = [...new Set(allEventTypes.map(e => e.event_type))];
	
	// Load simulation results from server on page load
	onMount(() => {
		loadSimulationResults();
	});
	
	async function loadSimulationResults() {
		try {
			loadingResults = true;
			const response = await fetch('http://localhost:8001/api/v1/simulation-results');
			if (response.ok) {
				const data = await response.json();
				simulationResults = data.results || [];
				showResults = simulationResults.length > 0;
			}
		} catch (err) {
			console.error('Error loading simulation results:', err);
		} finally {
			loadingResults = false;
		}
	}
	
	async function clearSimulationResults() {
		try {
			const response = await fetch('http://localhost:8001/api/v1/simulation-results', {
				method: 'DELETE'
			});
			if (response.ok) {
				simulationResults = [];
				showResults = false;
			}
		} catch (err) {
			console.error('Error clearing simulation results:', err);
			alert('Error clearing simulation results: ' + err.message);
		}
	}
	
	// Sequential simulation functionality
	async function runSequentialSimulation() {
		if (isSequentialRunning) return;
		
		isSequentialRunning = true;
		
		try {
			// Combine and sort all events by timestamp
			const allEvents = [
				...computerVisionMockData.map(e => ({
					...e,
					source: 'computer_vision',
					timestamp_key: 'creation_time',
					sort_time: new Date(e.creation_time).getTime()
				})),
				...accessControlMockData.map(e => ({
					...e,
					source: 'access_control',
					timestamp_key: 'timestamp',
					sort_time: new Date(e.timestamp).getTime()
				}))
			].sort((a, b) => a.sort_time - b.sort_time);
			
			let processedCount = 0;
			let results = [];
			
			for (const event of allEvents) {
				try {
					// Prepare event data for API
					const eventData = {
						event_type: event.event_type,
						event_details: `Sequential simulation: ${event.event_type}`,
						source: event.source,
						location: event.location,
						severity: event.severity,
						timestamp: event[event.timestamp_key],
						...(event.source === 'computer_vision' && {
							confidence: event.confidence,
							camera_id: event.camera_id
						}),
						...(event.source === 'access_control' && {
							badge_id: event.badge_id,
							door_id: event.door_id,
							access_level_required: event.access_level_required
						})
					};
					
					const response = await fetch('http://localhost:8001/api/v1/events/process', {
						method: 'POST',
						headers: { 'Content-Type': 'application/json' },
						body: JSON.stringify(eventData)
					});
					
					if (response.ok) {
						const result = await response.json();
						results.push({
							event: event.event_type,
							location: event.location,
							matched_sop: result.matched_sop,
							confidence: result.confidence,
							priority: result.priority,
							response_time: result.response_time,
							assigned_agents: result.assigned_agents,
							actions_required: result.actions_required,
							correlation_triggered: result.correlation_triggered,
							correlation_id: result.correlation_id,
							correlation_risk: result.correlation_risk
						});
						processedCount++;
					}
					
					// Add delay to simulate real-time processing
					await new Promise(resolve => setTimeout(resolve, 1000));
					
				} catch (err) {
					console.error(`Error processing event ${event.event_type}:`, err);
				}
			}
			
			// Reload results from server to get all processed events
			await loadSimulationResults();
				
		} catch (err) {
			alert('Sequential simulation error: ' + (err instanceof Error ? err.message : 'Unknown error'));
		} finally {
			isSequentialRunning = false;
		}
	}
	
	async function simulateEvent() {
		if (!selectedEvent) {
			alert('Please select an event type to simulate');
			return;
		}
		
		try {
			isSimulating = true;
			// Find a matching mock event from combined data
			const matchingEvent = allEventTypes.find(e => e.event_type === selectedEvent);
			
			if (!matchingEvent) {
				alert('Event type not found in mock data');
				return;
			}
			
			const mockEvent = {
				event_type: selectedEvent,
				event_details: `Simulated ${selectedEvent} event`,
				source: matchingEvent.source,
				location: matchingEvent.location,
				severity: matchingEvent.severity,
				timestamp: matchingEvent.source === 'computer_vision' ? matchingEvent.creation_time : matchingEvent.timestamp,
				...(matchingEvent.source === 'computer_vision' && {
					confidence: matchingEvent.confidence,
					camera_id: matchingEvent.camera_id
				}),
				...(matchingEvent.source === 'access_control' && {
					badge_id: matchingEvent.badge_id,
					door_id: matchingEvent.door_id,
					access_level_required: matchingEvent.access_level_required
				})
			};
			
			const response = await fetch('http://localhost:8001/api/v1/events/process', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(mockEvent)
			});
			
			if (response.ok) {
				const result = await response.json();
				
				// Add result to display
				const newResult = {
					id: Date.now() + Math.random(),
					event: selectedEvent,
					location: matchingEvent.location,
					matched_sop: result.matched_sop,
					confidence: result.confidence,
					priority: result.priority,
					response_time: result.response_time,
					assigned_agents: result.assigned_agents,
					actions_required: result.actions_required,
					correlation_triggered: result.correlation_triggered,
					correlation_id: result.correlation_id,
					correlation_risk: result.correlation_risk,
					timestamp: new Date().toLocaleTimeString(),
					type: 'single'
				};
				
				// Reload results from server to get the latest processed event
				await loadSimulationResults();
				
			} else {
				throw new Error('Failed to process event');
			}
		} catch (err) {
			alert('Error: ' + (err instanceof Error ? err.message : 'Unknown error'));
		} finally {
			isSimulating = false;
		}
	}
</script>

<svelte:head>
	<title>Event Simulator - SOP Agent</title>
</svelte:head>

<div class="space-y-6">
	<!-- Page Header -->
	<div>
		<h1 class="text-3xl font-bold text-gray-900">⚡ Event Simulator</h1>
		<p class="text-gray-600 mt-1">
			Test security event routing against uploaded SOPs
		</p>
	</div>
	
	<!-- Event Simulation -->
	<div class="card">
		<h2 class="text-xl font-semibold text-gray-900 mb-4">⚡ Event Simulation</h2>
		
		<!-- Event Type Selection -->
		<div class="mb-6">
			<label class="block text-sm font-medium text-gray-700 mb-2">Event Type</label>
			<select 
				bind:value={selectedEvent}
				class="input-field"
			>
				<option value="">Select an event type...</option>
				{#each allUniqueEvents as event}
					<option value={event}>{event}</option>
				{/each}
			</select>
		</div>
		
		<!-- Action Buttons -->
		<div class="flex flex-col sm:flex-row gap-3">
			<button 
				class="btn-primary flex-1"
				on:click={simulateEvent}
				disabled={!selectedEvent || isSimulating || isSequentialRunning}
			>
				{#if isSimulating}
					⏳ Processing...
				{:else}
					🚀 Simulate Single Event
				{/if}
			</button>
			
			<button 
				class="btn-secondary flex-1"
				on:click={runSequentialSimulation}
				disabled={isSequentialRunning}
			>
				{#if isSequentialRunning}
					⏳ Running Sequential...
				{:else}
					📊 Run Sequential Simulation
				{/if}
			</button>
			
			{#if showResults}
				<button 
					class="btn-danger"
					on:click={clearSimulationResults}
					disabled={isSequentialRunning}
				>
					🗑️ Clear Results
				</button>
			{/if}
		</div>
		
		{#if isSequentialRunning}
			<div class="mt-4 text-center py-4">
				<div class="animate-spin text-2xl mb-2">⟳</div>
				<p class="text-sm text-gray-600">Processing events...</p>
			</div>
		{/if}
	</div>
	
	<!-- Simulation Results -->
	{#if loadingResults}
		<div class="card">
			<div class="text-center py-8">
				<div class="animate-spin text-2xl mb-2">⟳</div>
				<p class="text-gray-500">Loading simulation results...</p>
			</div>
		</div>
	{:else if showResults && simulationResults.length > 0}
		<div class="card">
			<div class="flex justify-between items-center mb-4">
				<h2 class="text-xl font-semibold text-gray-900">🎯 Simulation Results ({simulationResults.length})</h2>
				<span class="text-sm text-gray-500">
					Persisted until server restart
				</span>
			</div>
			
			<div class="space-y-3">
				{#each simulationResults as result}
					<div class="border border-gray-200 rounded-lg p-4 bg-gray-50">
						<div class="flex justify-between items-start mb-2">
							<div class="flex items-center gap-2">
								<span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
									{result.type}
								</span>
								<h3 class="font-medium text-gray-900">{result.event}</h3>
								<span class="text-sm text-gray-500">@ {result.location}</span>
							</div>
							<span class="text-xs text-gray-400">{result.timestamp}</span>
						</div>
						
						<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-3">
							<div>
								<span class="text-sm font-medium text-gray-700">Matched SOP:</span>
								<p class="text-sm text-gray-900">{result.matched_sop}</p>
							</div>
							<div>
								<span class="text-sm font-medium text-gray-700">Priority:</span>
								<span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium {result.priority === 'High' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'}">
									{result.priority}
								</span>
							</div>
							<div>
								<span class="text-sm font-medium text-gray-700">Confidence:</span>
								<span class="text-sm text-gray-900">{(result.confidence * 100).toFixed(1)}%</span>
							</div>
						</div>
						
						{#if result.correlation_triggered}
							<div class="bg-orange-50 border border-orange-200 rounded-lg p-3 mb-3">
								<div class="flex items-center gap-2 mb-1">
									<span class="text-sm font-medium text-orange-800">🔍 AI Correlation Analysis</span>
									<span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
										{result.correlation_risk} Risk
									</span>
								</div>
								<p class="text-sm text-orange-700">
									Correlation ID: {result.correlation_id}
								</p>
								<p class="text-sm text-orange-600 mt-1">
									<a href="/threats/access-control" class="underline hover:text-orange-800">
										View detailed analysis in Threats page →
									</a>
								</p>
							</div>
						{/if}
						
						<div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
							<div>
								<span class="font-medium text-gray-700">Response Time:</span>
								<span class="text-gray-900">{result.response_time}</span>
							</div>
							<div>
								<span class="font-medium text-gray-700">Assigned Agents:</span>
								<span class="text-gray-900">{result.assigned_agents ? result.assigned_agents.join(', ') : 'None'}</span>
							</div>
						</div>
						
						{#if result.actions_required && result.actions_required.length > 0}
							<div class="mt-3">
								<span class="text-sm font-medium text-gray-700">Actions Required:</span>
								<ul class="text-sm text-gray-900 mt-1 ml-4">
									{#each result.actions_required as action}
										<li class="list-disc">{action}</li>
									{/each}
								</ul>
							</div>
						{/if}
					</div>
				{/each}
			</div>
		</div>
	{/if}
	
</div>