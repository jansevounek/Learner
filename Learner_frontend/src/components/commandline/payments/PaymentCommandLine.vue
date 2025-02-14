<template>
    <div class="cmd-line-container">
        <div class="cmd-output-container">
            {{ executedCommands }}
        </div>
        <div class="cmd-line-input-container">
            <h1 id="inputTitle">></h1>
            <input type="text" class="cmd-input" id="cmd-input" v-on:keyup.enter="executeCommand" ref="input" v-model="cmdinput">
        </div>
        <button class="cmd-input-mobile-btn" @click="executeCommand">
            Execute
        </button>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { supabase } from '@/supabase/init.js'
import { loadStripe } from '@stripe/stripe-js';
import { getUser } from '@/supabase/getFunctions.js'

// router import a setup
import { useRouter } from 'vue-router'
const router = useRouter()

const input = ref(null)

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY)

let executedCommands = ref('To continue type "pay":')
let cmdinput = ref('')

onMounted(() => {
    input.value?.focus()
    window.addEventListener('keydown', handleKeyDown);
    document.addEventListener('click', handleClick);
})

onUnmounted(() => {
    window.removeEventListener('keydown', handleKeyDown);
    document.removeEventListener('click', handleClick);
})

function executeCommand() {
    switch(cmdinput.value) {
        case "Logout":
        case "go 6":
            logout()
            break
        case "Lets Learn":
        case "go 7":
            router.push('/learning/manage')
            break
        case "Home":
        case "go 1":
            router.push('/')
            break

        // navbar bottom
        case "Github":
            window.location.replace("https://github.com/jansevounek/Learner");
            break
        case "Socials":
            window.location.replace("https://instagram.com");
            break
        case "License":
            window.location.replace("https://www.youtube.com/watch?v=xvFZjo5PgG0");
            break
        case "Get Premium":
            router.push('/payment/getpremium')
            break

        case "clear":
            clearLines()
            break
        
        case "pay":
            createCheckout()
            break

        case "":
            noCommand()
            break

        default:
            commandError()
    }
}

function clearLines() {
    executedCommands.value = 'To continue type "pay":'
    cmdinput.value = ''
}

function commandError() {
    executedCommands.value += "\n > " + cmdinput.value + '\n Command: "' + cmdinput.value + '" is not recognised as a command that can be used \n To continue type "pay": '
    cmdinput.value = ""
}

function handleKeyDown(event) {
    if (event.ctrlKey && event.key === 'l') {
        event.preventDefault();
        clearLines()    
    }
}

// handles if the user clicks somewhere
function handleClick() {
    document.getElementById('cmd-input').focus();
}

async function logout(){
    const { error } = await supabase.auth.signOut();
    if (error) {
        console.log(error.message)
    } else {
        router.push('/')
        location.reload()
    }
}

async function createCheckout() {
    const user = await getUser()
    const apiurl = import.meta.env.VITE_API_URL
    const response = await fetch(apiurl + "/payments/create-stripe-session", {
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