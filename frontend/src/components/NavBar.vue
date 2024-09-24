<template>
  <div>
<!-- navbar goes here -->
<nav class="font-sans bg-nav-blue">
  <div class="max-w-6xl mx-auto px-4">
    <div class="flex justify-between">

      <div class="flex space-x-4">
        <!-- logo -->
        <div>
          <router-link to="/" class="flex items-center py-5 px-2 text-gray-700 hover:text-gray-900">
            <img class="h-10 w-10 mr-1 text-blue-400" src="../assets/logo.png">
          </router-link>
        </div>

        <!-- primary nav -->
        <div class="font-sans md:flex items-center space-x-1">
          <router-link to="/" class="py-5 px-3 text-white hover:underline">Home</router-link>
          <router-link to="/profile" class="py-5 px-3 text-white hover:underline">Profile</router-link>
        </div>
      </div>

      <!-- secondary nav -->
      <div class="md:flex items-center space-x-1 text-white">
        <a href="logout/" class="py-2 px-3 hover:text-red-500">Logout</a>
      </div>


    </div>
  </div>
</nav>

  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AddItem from './AddItem.vue';

export default defineComponent({
    components: { AddItem },
  
})
</script>

