<template>
    <div class="title-container">
        <pre class="ascii-container text-[10px] lg:text-[20px]" id="ascii-art">
 ________  _______   ___       _______   ________ _________   
|\   ____\|\  ___ \ |\  \     |\  ___ \ |\   ____\\___   ___\ 
\ \  \___|\ \   __/|\ \  \    \ \   __/|\ \  \___\|___ \  \_| 
 \ \_____  \ \  \_|/_\ \  \    \ \  \_|/_\ \  \       \ \  \  
  \|____|\  \ \  \_|\ \ \  \____\ \  \_|\ \ \  \____   \ \  \ 
    ____\_\  \ \_______\ \_______\ \_______\ \_______\  \ \__\
   |\_________\|_______|\|_______|\|_______|\|_______|   \|__|
   \|_________|                                               
        </pre>
        <p class="title-ps-text">what you want to learn</p>
        <p class="title-warning-text">On this page you can now select what you want to start learning</p>
        <hr class="title-hr">
    </div>
    <div class="top-16 relative w-screen">
        <LectionCommandLine />
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import LectionCommandLine from '../components/commandline/LectionCommandLine.vue'

// generates the random color for the title
onMounted(() => {
    const random = Math.floor(Math.random() * 5);
    const colors = ["text-blue-600", "text-green-600", "text-red-600", "text-orange-600", "text-violet-600",];
    const ascii = document.getElementById("ascii-art")
    ascii.classList.add(colors[random])
})
</script>