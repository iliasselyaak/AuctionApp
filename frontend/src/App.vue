<template>
    <div class="font-sans">
        <NavBar/>
        <router-view/> 
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue'
  import NavBar from './components/NavBar.vue';
  import Home from './components/Home.vue';
  
  export default defineComponent({
      components: { NavBar,Home },
  })
  </script>
  
  