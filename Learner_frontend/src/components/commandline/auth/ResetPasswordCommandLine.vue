<template>
    <div class="top-16 relative flex flex-col text-green-600 font-mono mx-4">
        <div class="cmd-output-container">
            {{ executedCommands }}
        </div>
        <div class="flex flex-row">
            <p>></p>
            <input type="email" class="cmd-input" v-model="cmdinput" id="cmd-input" v-on:keyup.enter="executeCommand" ref="input" :class="[{'text-red-600': isEmail === false}]">
        </div>
        <button class="cmd-input-mobile-btn" @click="executeCommand">
            Execute
        </button>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { supabase } from '@/supabase/init.js'

// router import a setup
import { useRouter } from 'vue-router'
const router = useRouter()

let executedCommands = ref('Please enter your email adress:')
let cmdinput = ref('')

const input = ref(null)

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
        case "Signup":
        case "go 3":
            router.push('/signup')
            break
        case "Login":
        case "go 2":
            router.push('/login')
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
        
        default:
            trySendEmail()
    }
}

function trySendEmail() {
    const email = cmdinput.value
    cmdinput.value = ''
    if(testEmail(email)){
        sendEmail(email)
    } else {
        commandOutput("This is not a valid email adress")
    }
}

async function sendEmail(email) {
    const { data, error } = await supabase.auth.resetPasswordForEmail(email, {
        redirectTo: 'https://127.0.0.1:5173/updateuser',
    })
    if (error) {
        console.log(error)
    }
    
    commandOutput("Your email has been sent")
}

const isEmail = computed(() => {
    if (cmdinput.value === '') {
        return true
    }
    return testEmail(cmdinput.value)
})

function testEmail(email) {
    return /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(email)
}

function commandOutput(output) {
    executedCommands.value +=  " \n >  "+ cmdinput.value + "\n" +
                        output + "\n \n" + "Please enter your email adress:"
    cmdinput.value = ""
}


// handles the "ctrl + c" shortcut
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

</script>