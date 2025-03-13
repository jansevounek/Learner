<template>
    <div class="title-container">
        <pre class="ascii-container" id="ascii-art">
 _____                __        
|     |_.-----.-----.|__|.-----.
|       |  _  |  _  ||  ||     |
|_______|_____|___  ||__||__|__|
              |_____|           
        </pre>
        <p class="title-warning-text">This is the login page you will be asked for your information one by one by the titles below (The first one is "Username:")</p>
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
    const colors = ["dark:text-blue-600", "dark:text-green-600", "dark:text-red-600", "dark:text-orange-600", "dark:text-violet-600",];
    const ascii = document.getElementById("ascii-art")
    ascii.classList.add(colors[random])
})
</script>