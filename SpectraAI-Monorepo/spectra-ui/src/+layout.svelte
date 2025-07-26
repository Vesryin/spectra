<script lang="ts">
  import '../app.css';
  import { onMount } from 'svelte';
  
  let mounted = false;
  
  onMount(() => {
    mounted = true;
  });
</script>

<svelte:head>
  <title>SpectraAI - Advanced AI Assistant</title>
</svelte:head>

<div class="app" class:mounted>
  <slot />
</div>

<style>
  .app {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    opacity: 0;
    transition: opacity 0.3s ease-in-out;
  }
  
  .app.mounted {
    opacity: 1;
  }
</style>
