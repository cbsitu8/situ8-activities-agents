<script lang="ts">
	import '../app.css';
	
	// Navigation state
	let currentPage = 'sop-manager';
	
	const navigation = [
		{ id: 'sop-manager', name: 'SOP Manager', href: '/sop-manager', icon: '📄' },
		{ id: 'event-simulator', name: 'Event Simulator', href: '/event-simulator', icon: '⚡' },
		{ id: 'threats', name: 'Access Control Threats', href: '/threats/access-control', icon: '🚨' }
	];
</script>

<div class="min-h-screen bg-gray-50">
	<!-- Navigation Header -->
	<nav class="bg-white shadow-sm border-b border-gray-200">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
			<div class="flex justify-between items-center h-16">
				<!-- Logo and Title -->
				<div class="flex items-center">
					<div class="flex-shrink-0">
						<h1 class="text-xl font-bold text-gray-900">🛡️ SOP Agent</h1>
					</div>
					<div class="ml-4">
						<p class="text-sm text-gray-500">Security Operations Platform</p>
					</div>
				</div>
				
				<!-- Navigation Links -->
				<div class="flex space-x-4">
					{#each navigation as item}
						<a
							href={item.href}
							class="flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors
								{currentPage === item.id 
									? 'bg-sop-primary text-white' 
									: 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'}"
							on:click={() => currentPage = item.id}
						>
							<span class="mr-2">{item.icon}</span>
							{item.name}
						</a>
					{/each}
				</div>
			</div>
		</div>
	</nav>
	
	<!-- Main Content -->
	<main class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
		<slot />
	</main>
	
	<!-- Footer -->
	<footer class="bg-white border-t border-gray-200 mt-12">
		<div class="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
			<div class="flex justify-between items-center">
				<p class="text-sm text-gray-500">
					SOP-Enhanced Agentic Security Operations System v1.0.0
				</p>
				<div class="flex space-x-4 text-sm text-gray-500">
					<span>🟢 Services: Online</span>
					<span>⚡ Response Time: &lt;50ms</span>
				</div>
			</div>
		</div>
	</footer>
</div>