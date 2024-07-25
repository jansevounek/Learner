<template>
    <div class="title-container">
        <pre class="ascii-container" id="ascii-art1">
 __    ____    __    ____  _  _   
(  )  ( ___)  /__\  (  _ \( \( )  
 )(__  )__)  /(__)\  )   / )  (   
(____)(____)(__)(__)(_)\_)(_)\_)  
        </pre>
        <pre class="ascii-container text-[10px] lg:text-sm" id="ascii-art2">
      ___           ___           ___     
     /\  \         /\  \         /\  \    
     \:\  \       /::\  \       _\:\  \   
      \:\  \     /:/\:\  \     /\ \:\  \  
  _____\:\  \   /:/  \:\  \   _\:\ \:\  \ 
 /::::::::\__\ /:/__/ \:\__\ /\ \:\ \:\__\
 \:\~~\~~\/__/ \:\  \ /:/  / \:\ \:\/:/  /
  \:\  \        \:\  /:/  /   \:\ \::/  / 
   \:\  \        \:\/:/  /     \:\/:/  /  
    \:\__\        \::/  /       \::/  /   
     \/__/         \/__/         \/__/    
        </pre>
        <p class="title-warning-text">This is the page from where tou navigate around the learning part of the applycation</p>
        <p class="title-ps-text">PS: try typing "help"</p>
        <hr class="title-hr">
    </div>
    <div class="main-container">
        <LearningHomeCommandLine />
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import LearningHomeCommandLine from '../components/commandline/LearningHomeCommandLine.vue'

// generates the random color for the title
onMounted(() => {
    const random = Math.floor(Math.random() * 5);
    const colors1 = ["text-blue-600", "text-green-600", "text-red-600", "text-orange-600", "text-violet-600",];
    const colors2 = ["text-violet-600", "text-orange-600", "text-blue-600", "text-green-600", "text-red-600",];
    const ascii1 = document.getElementById("ascii-art1")
    const ascii2 = document.getElementById("ascii-art2")
    ascii1.classList.add(colors1[random])
    ascii2.classList.add(colors2[random])
})
</script>