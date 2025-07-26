<script lang="ts">
  import { onMount } from 'svelte';
  import { Brain, MessageCircle, Heart, Memory, Zap } from 'lucide-svelte';
  import ChatInterface from '$lib/components/ChatInterface.svelte';
  import SystemStatus from '$lib/components/SystemStatus.svelte';
  
  let currentView: 'home' | 'chat' | 'status' = 'home';
  let isLoaded = false;
  
  onMount(() => {
    setTimeout(() => {
      isLoaded = true;
    }, 100);
  });
  
  const features = [
    {
      icon: Brain,
      title: 'Advanced AI Brain',
      description: 'Powered by OpenHermes-2.5-Mistral-7B for intelligent conversations'
    },
    {
      icon: Heart,
      title: 'Emotional Intelligence',
      description: 'Real-time emotion processing and empathetic responses'
    },
    {
      icon: Memory,
      title: 'Persistent Memory',
      description: 'Remembers context and builds lasting relationships'
    },
    {
      icon: Zap,
      title: 'Real-time Processing',
      description: 'Lightning-fast responses with WebSocket connectivity'
    }
  ];
</script>

<svelte:head>
  <title>SpectraAI - Advanced AI Assistant</title>
  <meta name="description" content="Experience the future of AI with SpectraAI - featuring advanced memory, emotions, and personality" />
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
  <!-- Navigation -->
  <nav class="backdrop-blur-sm bg-white/30 border-b border-white/20 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-gradient-to-br from-spectra-500 to-spectra-600 rounded-xl flex items-center justify-center shadow-lg">
            <Brain class="w-6 h-6 text-white" />
          </div>
          <h1 class="text-2xl font-bold gradient-text">SpectraAI</h1>
        </div>
        
        <div class="flex space-x-4">
          <button 
            on:click={() => currentView = 'home'}
            class="px-4 py-2 rounded-lg transition-all duration-200 hover:bg-white/20 border border-transparent hover:border-white/30"
            class:bg-white/20={currentView === 'home'}
            class:border-white/30={currentView === 'home'}
          >
            Home
          </button>
          <button 
            on:click={() => currentView = 'chat'}
            class="px-4 py-2 rounded-lg transition-all duration-200 hover:bg-white/20 border border-transparent hover:border-white/30 flex items-center space-x-2"
            class:bg-white/20={currentView === 'chat'}
            class:border-white/30={currentView === 'chat'}
          >
            <MessageCircle class="w-4 h-4" />
            <span>Chat</span>
          </button>
          <button 
            on:click={() => currentView = 'status'}
            class="px-4 py-2 rounded-lg transition-all duration-200 hover:bg-white/20 border border-transparent hover:border-white/30"
            class:bg-white/20={currentView === 'status'}
            class:border-white/30={currentView === 'status'}
          >
            Status
          </button>
        </div>
      </div>
    </div>
  </nav>

  <!-- Main Content -->
  <main class="flex-1">
    {#if currentView === 'home'}
      <!-- Hero Section -->
      <section class="relative py-20 px-4 sm:px-6 lg:px-8">
        <div class="max-w-4xl mx-auto text-center">
          <div class="space-y-8" class:animate-float={isLoaded}>
            <div class="space-y-4">
              <h2 class="text-5xl sm:text-6xl font-bold gradient-text">
                Meet SpectraAI
              </h2>
              <p class="text-xl text-slate-600 max-w-2xl mx-auto">
                The next generation of AI assistants with advanced memory, emotional intelligence, and adaptive personality
              </p>
            </div>
            
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
              <button 
                on:click={() => currentView = 'chat'}
                class="px-8 py-4 bg-gradient-to-r from-spectra-500 to-spectra-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200 animate-glow"
              >
                Start Chatting
              </button>
              <button 
                on:click={() => currentView = 'status'}
                class="px-8 py-4 bg-white/50 backdrop-blur-sm border border-white/30 rounded-xl font-semibold hover:bg-white/70 transition-all duration-200"
              >
                View System Status
              </button>
            </div>
          </div>
        </div>
        
        <!-- Animated Background Elements -->
        <div class="absolute inset-0 overflow-hidden pointer-events-none">
          <div class="absolute top-1/4 left-1/4 w-32 h-32 bg-spectra-200/30 rounded-full blur-xl animate-pulse-slow"></div>
          <div class="absolute top-3/4 right-1/4 w-24 h-24 bg-indigo-200/30 rounded-full blur-xl animate-pulse-slow" style="animation-delay: 1s;"></div>
          <div class="absolute top-1/2 right-1/3 w-16 h-16 bg-blue-200/30 rounded-full blur-xl animate-pulse-slow" style="animation-delay: 2s;"></div>
        </div>
      </section>

      <!-- Features Section -->
      <section class="py-20 px-4 sm:px-6 lg:px-8">
        <div class="max-w-6xl mx-auto">
          <div class="text-center mb-16">
            <h3 class="text-3xl font-bold text-slate-800 mb-4">
              Advanced AI Capabilities
            </h3>
            <p class="text-lg text-slate-600 max-w-2xl mx-auto">
              SpectraAI combines cutting-edge technology with intuitive design to deliver an unparalleled AI experience
            </p>
          </div>
          
          <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {#each features as feature, i}
              <div 
                class="glass rounded-2xl p-6 hover:bg-white/20 transition-all duration-300 group transform hover:-translate-y-2"
                style="animation-delay: {i * 0.1}s;"
                class:opacity-0={!isLoaded}
                class:animate-[slideUp_0.6s_ease-out_forwards]={isLoaded}
              >
                <div class="w-12 h-12 bg-gradient-to-br from-spectra-500 to-spectra-600 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-200">
                  <svelte:component this={feature.icon} class="w-6 h-6 text-white" />
                </div>
                <h4 class="text-xl font-semibold text-slate-800 mb-2">{feature.title}</h4>
                <p class="text-slate-600">{feature.description}</p>
              </div>
            {/each}
          </div>
        </div>
      </section>

      <!-- Stats Section -->
      <section class="py-16 px-4 sm:px-6 lg:px-8 bg-white/30 backdrop-blur-sm">
        <div class="max-w-4xl mx-auto">
          <div class="grid md:grid-cols-3 gap-8 text-center">
            <div class="space-y-2">
              <div class="text-4xl font-bold gradient-text">7B</div>
              <div class="text-slate-600">Parameters in AI Model</div>
            </div>
            <div class="space-y-2">
              <div class="text-4xl font-bold gradient-text">∞</div>
              <div class="text-slate-600">Memory Capacity</div>
            </div>
            <div class="space-y-2">
              <div class="text-4xl font-bold gradient-text">2025</div>
              <div class="text-slate-600">Modern Tech Stack</div>
            </div>
          </div>
        </div>
      </section>
    {:else if currentView === 'chat'}
      <ChatInterface />
    {:else if currentView === 'status'}
      <SystemStatus />
    {/if}
  </main>

  <!-- Footer -->
  <footer class="bg-white/30 backdrop-blur-sm border-t border-white/20 py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto text-center">
      <p class="text-slate-600">
        SpectraAI &copy; 2025 - Advanced AI Assistant with Memory, Emotions, and Personality
      </p>
      <p class="text-sm text-slate-500 mt-2">
        Powered by OpenHermes-2.5-Mistral-7B | Built with SvelteKit & FastAPI
      </p>
    </div>
  </footer>
</div>

<style>
  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(30px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>
