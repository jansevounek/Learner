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
        <p class="title-warning-text">Here you can pay for the premium version of our application</p>
        <p class="title-ps-text">It includes ...</p>
        <hr class="title-hr">
    </div>
    <div class="top-16 relative w-screen">
        <StripeCheckout />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { StripeCheckout } from '@vue-stripe/vue-stripe';

// generates the random color for the title
onMounted(() => {
    const random = Math.floor(Math.random() * 5);
    const colors = ["text-blue-600", "text-green-600", "text-red-600", "text-orange-600", "text-violet-600",];
    const ascii = document.getElementById("ascii-art")
    ascii.classList.add(colors[random])
})
</script>