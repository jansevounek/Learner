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
import { supabase } from './supabase/init.js'


// Taken from https://supabase.com/docs/guides/realtime?queryGroups=language&language=js
const handleInserts = (payload) => {
    console.log('Change received!', payload)
}

supabase
  .channel('user_extra')
  .on('postgres_changes', { event: '*', schema: 'public', table: 'user_extra' }, handleInserts)
  .subscribe()
</script>

