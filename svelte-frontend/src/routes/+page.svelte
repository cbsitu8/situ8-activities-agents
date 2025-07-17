<script>
	import { onMount } from 'svelte';
	
	let serviceStatus = {
		postgres: 'checking',
		python: 'checking',
		go: 'checking'
	};
	
	onMount(async () => {
		// Check service health
		await checkServices();
	});
	
	async function checkServices() {
		// Check Python service
		try {
			const response = await fetch('http://localhost:8001/api/v1/health');
			serviceStatus.python = response.ok ? 'online' : 'offline';
		} catch {
			serviceStatus.python = 'offline';
		}
		
		// Check Go service
		try {
			const response = await fetch('http://localhost:8080/api/v1/health');
			serviceStatus.go = response.ok ? 'online' : 'offline';
		} catch {
			serviceStatus.go = 'offline';
		}
		
		// PostgreSQL status is checked via Python service
		serviceStatus.postgres = serviceStatus.python === 'online' ? 'online' : 'offline';
		
		// Trigger reactivity
		serviceStatus = { ...serviceStatus };
	}
	
	function getStatusColor(status) {
		switch (status) {
			case 'online': return 'text-green-600';
			case 'offline': return 'text-red-600';
			default: return 'text-yellow-600';
		}
	}
	
	function getStatusIcon(status) {
		switch (status) {
			case 'online': return '🟢';
			case 'offline': return '🔴';
			default: return '🟡';
		}
	}
</script>

<svelte:head>
	<title>SOP Agent - Home</title>
</svelte:head>

<div class="space-y-8">
	<!-- Hero Section -->
	<div class="text-center">
		<h1 class="text-4xl font-bold text-gray-900 mb-4">
			🛡️ SOP-Enhanced Agentic Security Operations System
		</h1>
		<p class="text-xl text-gray-600 max-w-3xl mx-auto">
			Intelligent security event routing using organizational Standard Operating Procedures. 
			Route events in &lt;50ms with deterministic, SOP-based decision making.
		</p>
	</div>
	
	<!-- Service Status -->
	<div class="bg-white rounded-lg shadow-md p-6">
		<h2 class="text-2xl font-semibold text-gray-900 mb-4 flex items-center">
			⚙️ System Status
			<button 
				class="ml-4 text-sm btn-secondary"
				on:click={checkServices}
			>
				Refresh
			</button>
		</h2>
		
		<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
			<div class="border rounded-lg p-4">
				<div class="flex items-center justify-between">
					<div>
						<h3 class="font-medium text-gray-900">PostgreSQL Database</h3>
						<p class="text-sm text-gray-500">SOPs, Rules & Embeddings</p>
					</div>
					<div class="text-right">
						<span class={`font-medium ${getStatusColor(serviceStatus.postgres)}`}>
							{getStatusIcon(serviceStatus.postgres)} {serviceStatus.postgres}
						</span>
					</div>
				</div>
			</div>
			
			<div class="border rounded-lg p-4">
				<div class="flex items-center justify-between">
					<div>
						<h3 class="font-medium text-gray-900">Python SOP Service</h3>
						<p class="text-sm text-gray-500">Document Processing & AI</p>
					</div>
					<div class="text-right">
						<span class={`font-medium ${getStatusColor(serviceStatus.python)}`}>
							{getStatusIcon(serviceStatus.python)} {serviceStatus.python}
						</span>
						<p class="text-xs text-gray-400">Port 8001</p>
					</div>
				</div>
			</div>
			
			<div class="border rounded-lg p-4">
				<div class="flex items-center justify-between">
					<div>
						<h3 class="font-medium text-gray-900">Go Routing Engine</h3>
						<p class="text-sm text-gray-500">Event Processing & Rules</p>
					</div>
					<div class="text-right">
						<span class={`font-medium ${getStatusColor(serviceStatus.go)}`}>
							{getStatusIcon(serviceStatus.go)} {serviceStatus.go}
						</span>
						<p class="text-xs text-gray-400">Port 8080</p>
					</div>
				</div>
			</div>
		</div>
	</div>
	
	<!-- Feature Overview -->
	<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
		<!-- SOP Manager -->
		<div class="card">
			<div class="flex items-center mb-4">
				<div class="text-3xl mr-3">📄</div>
				<h2 class="text-2xl font-semibold text-gray-900">SOP Manager</h2>
			</div>
			<p class="text-gray-600 mb-4">
				Upload and manage Standard Operating Procedures. Extract rules and generate semantic embeddings for intelligent event routing.
			</p>
			<ul class="text-sm text-gray-600 space-y-2 mb-6">
				<li>✅ Drag & drop .docx/.md files</li>
				<li>✅ Automatic rule extraction</li>
				<li>✅ Semantic embedding generation</li>
				<li>✅ Rule visualization & management</li>
			</ul>
			<a href="/sop-manager" class="btn-primary">
				Open SOP Manager
			</a>
		</div>
		
		<!-- Event Simulator -->
		<div class="card">
			<div class="flex items-center mb-4">
				<div class="text-3xl mr-3">⚡</div>
				<h2 class="text-2xl font-semibold text-gray-900">Event Simulator</h2>
			</div>
			<p class="text-gray-600 mb-4">
				Test event routing against SOPs. Load CSV data and simulate security events with real-time processing feedback.
			</p>
			<ul class="text-sm text-gray-600 space-y-2 mb-6">
				<li>✅ CSV data loading</li>
				<li>✅ Real-time event processing</li>
				<li>✅ SOP matching visualization</li>
				<li>✅ Performance metrics</li>
			</ul>
			<a href="/event-simulator" class="btn-primary">
				Open Event Simulator
			</a>
		</div>
	</div>
	
	<!-- Architecture Overview -->
	<div class="card">
		<h2 class="text-2xl font-semibold text-gray-900 mb-4">🏗️ System Architecture</h2>
		<div class="bg-gray-50 rounded-lg p-6">
			<div class="grid grid-cols-1 md:grid-cols-4 gap-4 text-center">
				<div class="bg-white rounded-lg p-4 border">
					<div class="text-2xl mb-2">📱</div>
					<h3 class="font-medium">Svelte Frontend</h3>
					<p class="text-sm text-gray-500">Port 3005</p>
				</div>
				<div class="bg-white rounded-lg p-4 border">
					<div class="text-2xl mb-2">🐍</div>
					<h3 class="font-medium">Python SOP Service</h3>
					<p class="text-sm text-gray-500">Port 8001</p>
				</div>
				<div class="bg-white rounded-lg p-4 border">
					<div class="text-2xl mb-2">🚀</div>
					<h3 class="font-medium">Go Routing Engine</h3>
					<p class="text-sm text-gray-500">Port 8080</p>
				</div>
				<div class="bg-white rounded-lg p-4 border">
					<div class="text-2xl mb-2">🗄️</div>
					<h3 class="font-medium">PostgreSQL + pgvector</h3>
					<p class="text-sm text-gray-500">Port 5432</p>
				</div>
			</div>
		</div>
	</div>
</div>