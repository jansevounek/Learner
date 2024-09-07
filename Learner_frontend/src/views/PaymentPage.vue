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
        <button @click="createCheckout">Pay now</button>
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { loadStripe } from '@stripe/stripe-js';
import { supabase } from '../supabase/init.js'

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY)

// generates the random color for the title
onMounted(() => {
    const random = Math.floor(Math.random() * 5);
    const colors = ["text-blue-600", "text-green-600", "text-red-600", "text-orange-600", "text-violet-600",];
    const ascii = document.getElementById("ascii-art")
    ascii.classList.add(colors[random])
})

// taken from https://docs.vuestripe.com/vue-stripe/stripe-checkout/one-time-payment and https://www.youtube.com/watch?v=g2Dtt4_dQQ4
//TODO steup webhook on stripe
async function submit() {
    const { data: { user } } = await supabase.auth.getUser()
    checkoutRef.value.redirectToCheckout({
        metadata: user.id
    })
}

async function createCheckout() {
    const { data: { user } } = await supabase.auth.getUser()
    const apiurl = import.meta.env.VITE_API_URL
    const response = await fetch(apiurl + "/create-stripe-session", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(user.id),
    });
    
    if (response) {
        const stripe = await stripePromise
        const data = await response.json()
        const sessionId = data.sessionId
        await stripe.redirectToCheckout({ sessionId });
    }
}
</script>