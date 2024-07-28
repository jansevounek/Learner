<template>
  <div class="w-[100%] h-screen bg-black">
    <NavBarTop />
    <RouterView />
    <NavBarBottom />
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import NavBarTop from './components/navbar/NavBarTop.vue'
import NavBarBottom from './components/navbar/NavBarBottom.vue'
</script>

