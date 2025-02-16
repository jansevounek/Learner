<template>
    <div class="cmd-line-container">
        <div class="cmd-output-container">
            {{ executedCommands }}
        </div>
        <div class="cmd-credential-input">
            <p class="cmd-credential-name">{{ inputName }}</p>
            <div class="cmd-line-input-container">
                <h1>></h1>
                <input :type="currentStep > 0 && currentStep < 3 ? 'password' : 'text'" class="cmd-input"  
                :class="[{'text-red-600': isEmail === false}]" id="cmd-input"
                v-on:keyup.enter="executeCommand" ref="input" v-model="cmdinput">
            </div>
            <div class="cmd-password-strength-container" v-if="showStrength">
                <p class="cmd-strength-indicator" :class="strengthLevel >= 2 ? 'text-red-600' : 'text-white'">#</p>
                <p class="cmd-strength-indicator" :class="strengthLevel >= 3 ? 'text-orange-600' : 'text-white'">#</p>
                <p class="cmd-strength-indicator" :class="strengthLevel >= 4 ? 'text-yellow-600' : 'text-white'">#</p>
                <p class="cmd-strength-indicator" :class="strengthLevel >= 5 ? 'text-green-600' : 'text-white'">#</p>
            </div>
        </div>
        <button class="cmd-input-mobile-btn" @click="executeCommand">
            Execute
        </button>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { supabase } from '@/supabase/init.js'

// import a setup of the router
import { useRouter, useRoute } from 'vue-router'
const router = useRouter()

const input = ref(null)

// mounting handlers for shortcuts
onMounted(() => {
    input.value?.focus()
    window.addEventListener('keydown', handleKeyDown);
    document.addEventListener('click', handleClick);
})

onUnmounted(() => {
    window.removeEventListener('keydown', handleKeyDown);
    document.removeEventListener('click', handleClick);
})

const cmdinput = ref('')
const executedCommands = ref('')

const inputName = ref('Email:')

const credentials = ref([])
const currentStep = ref(0)

// function that checks all the commands
function executeCommand() {
    switch(cmdinput.value) {

        // navbar commands
        case "Home":
        case "go 1":
            router.push('/')
            break
        case "Login":
        case "go 2":
            router.push('/login')
            break
        case "Signup":
        case "go 3":
            router.push('/signup')
            break
        case "Forgot Password?":
        case "go 5":
            router.push('/resetpassword')
            break
        case "go 6":
            logout()
            break

        // general commands
        case "help":
            getHelp()
            cmdinput.value = ''
            break
        case "clear":
            clearLines()
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

        default:
            processCredential()
    }
}

// processes the passwords and the username
function processCredential() {
    switch(currentStep.value) {
        case 0:
            saveEmail()
            break
        case 1:
            savePassword()
            break
        case 2:
            savePassword()
            break
        case 3:
            if(credentials.value[1] === credentials.value[2]) {
                changePassword()
            }
            cmdinput.value = ''
            break
    }
    console.log(currentStep.value)
    console.log(credentials.value)
}

// saves the password and other auth info
function savePassword() {
    if (currentStep.value == 1){
        if (strengthLevel.value == 5) {
            executedCommands.value += inputName.value + "\n" + "> " + '•'.repeat(cmdinput.value.length) + "\n"
            credentials.value[currentStep.value] = cmdinput.value
            currentStep.value++
            cmdinput.value = ''
            inputName.value = 'Repeat Password'
        } else {
            executedCommands.value += inputName.value + "\n" + "> " + '•'.repeat(cmdinput.value.length) + "\n" +
                                    "This password is not strong enough. Try adding special symbols, numbers and don't forget about length. \n"
            cmdinput.value = ''
        }
    } else {
        if (cmdinput.value === credentials.value[1]){
            executedCommands.value += inputName.value + "\n" + "> " + '•'.repeat(cmdinput.value.length) + "\n"
            credentials.value[currentStep.value] = cmdinput.value
            currentStep.value++
            cmdinput.value = ''
            inputName.value = 'Are you sure you want to change your password [Y/n]:'
        } else {
            executedCommands.value += inputName.value + "\n" + "> " + '•'.repeat(cmdinput.value.length) + "\n" +
                                    "The passwords provided do not match. Please try again \n"
            cmdinput.value = ''
        }
    }
}

function saveEmail() {
    if(testEmail(cmdinput.value)){
        console.log(isEmail.value)
        console.log('done')
        executedCommands.value += inputName.value + "\n" + "> " + cmdinput.value + "\n"
        credentials.value[currentStep.value] = cmdinput.value
        currentStep.value++
        cmdinput.value = ''
        inputName.value = "Password:"
    } else {
        executedCommands.value += inputName.value + "\n" + "> " + cmdinput.value + "\n" +
                                "This is not a valid email address. Please enter a valid one. \n"
        cmdinput.value = ''
    }
}

async function changePassword() {
    if (cmdinput.value == "Y"){
        const { data, error } = await supabase.auth.updateUser({
            email: credentials.value[0],
            password: credentials.value[1]
        })
        if (error){
            console.log(error)
        }
    } else {
        location.reload()
    }
}

async function logout() {
    const { error } = await supabase.auth.signOut();
    if (error) {
        console.log(error.message)
    } else {
        location.reload()
    }
}

const isEmail = computed(() => {
    if (currentStep.value == 0) {
        if (cmdinput.value === '') {
            return true
        }
        return testEmail(cmdinput.value)
    }
    return true
})

function testEmail(email) {
    return /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(email)
}

const passwordStrength = computed(() => {
    let score = -1
    if (currentStep.value == 1){
        score = 0

        let letters = {}
        for (let i = 0; i < cmdinput.value.length; i++) {
            letters[cmdinput.value[i]] = (letters[cmdinput.value[i]] || 0) + 1
            score += 5.0 / letters[cmdinput.value[i]]
        }

        let variations = {
            digits: /\d/.test(cmdinput.value),
            lower: /[a-z]/.test(cmdinput.value),
            upper: /[A-Z]/.test(cmdinput.value),
            nonWords: /\W/.test(cmdinput.value),
        };

        let variationCount = 0;
        for (let check in variations) {
            variationCount += (variations[check] === true) ? 1 : 0;
        }

        score += ((variationCount - 1) * 10);
    }

    return parseInt(score)
})

const strengthLevel = computed(() => {
    if (passwordStrength.value < 20) {
        return 1
    } else if (passwordStrength.value < 40) {
        return 2
    } else if (passwordStrength.value < 60) {
        return 3
    } else if (passwordStrength.value < 75) {
        return 4
    } else {
        return 5
    }
})

const showStrength = computed(() => {
    return currentStep.value == 1
})

// clears all the lines of output
function clearLines() {
    executedCommands.value = ''
    cmdinput.value = ''
}

// returns a string containing help info
function getHelp() {
    executedCommands.value = ''
    cmdinput.value = ''
    executedCommands.value += "Help: \n" +
                                "Help me \n"
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