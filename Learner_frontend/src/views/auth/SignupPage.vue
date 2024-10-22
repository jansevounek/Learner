<template>
    <div class="title-container">
        <pre class="ascii-container" id="ascii-art">
  _________.__                            
 /   _____/|__| ____   ____  __ ________  
 \_____  \ |  |/ ___\ /    \|  |  \____ \ 
 /        \|  / /_/  >   |  \  |  /  |_> >
/_______  /|__\___  /|___|  /____/|   __/ 
        \/   /_____/      \/      |__|    
        </pre>
        <p class="title-warning-text">This is the sinup page you will be asked for your information one by one by the titles below (The first one is "Username:")</p>
        <p class="title-ps-text">PS: When you are done you will be loged in and redirected</p>
        <hr class="title-hr">
    </div>
    <div class="main-container">
        <AuthCommandLine />
    </div>
</template>

<script setup>
import AuthCommandLine from '@/components/commandline/auth/AuthCommandLine.vue'
import { onMounted } from 'vue'  

// generates the random color for the title
onMounted(() => {
    const random = Math.floor(Math.random() * 5);
    const colors = ["text-blue-600", "text-green-600", "text-red-600", "text-orange-600", "text-violet-600",];
    const ascii = document.getElementById("ascii-art")
    ascii.classList.add(colors[random])
})
</script>