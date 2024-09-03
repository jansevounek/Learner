<template>
    <div class="cmd-line-container">
        <div class="cmd-output-container">
            {{ executedCommands }}
        </div>
        <div class="cmd-arrow-input">
            <p class="cmd-arrow-name">{{ inputName }}</p>
            <div class="cmd-line-input-container">
                <h1>></h1>
                <input :type="!showText ? 'password' : 'text'" class="cmd-input"  
                :class="[{'text-red-600': isEmail === false}]" id="cmd-input"
                 v-on:keyup.enter="executeCommand" v-model="cmdinput" autofocus>
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
import { supabase } from '../../supabase/init.js'

// import a setup of the router
import { useRouter, useRoute } from 'vue-router'
import { errorMessages } from 'vue/compiler-sfc';
const router = useRouter()
const route = useRoute()

// mounting handlers for shortcuts
onMounted(() => {
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

const showPassword = ref(false)

// function that checks all the commands
function executeCommand() {
    switch(cmdinput.value) {

        // navbar commands
        case "Home":
        case "navbar 1":
            router.push('/')
            break
        case "Login":
        case "navbar 2":
            router.push('/login')
            break
        case "Signup":
        case "navbar 3":
            router.push('/signup')
            break
        case "Forgot Password?":
        case "navbar 5":
            router.push('/resetpassword')
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

        // the stuff that logs you in
        case "google":
            loginWithGoogle()
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
                auth()
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
        if (strengthLevel.value == 5 || route.path == '/login') {
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
            inputName.value = 'Are you sure you want to log in [Y/n]:'
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

const isEmail = computed(() => {
    if (currentStep.value == 0) {
        if (cmdinput.value === '' || route.path === '/login') {
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

const showText = computed(() => {
    if (currentStep.value > 0 && currentStep.value < 3) {
        if (showPassword.value == true) {
            return true
        }
        return false
    }
    
    return true
})

const showStrength = computed(() => {
    return currentStep.value == 1 && route.path !== '/login'
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
                                "This is a website where you log in" +
                                "\n" +
                                'Follow the titles written above the ">" sign which signals the input and simply just write what the title asks for' +
                                "\n" +
                                "\n" +
                                'Additionally you can use the command "google" which lets you login with google'
}

// handles the "ctrl + c" shortcut
// TODO nobody knows what ctrl + i does
function handleKeyDown(event) {
    if (event.ctrlKey && event.key === 'l') {
        event.preventDefault();
        clearLines()    
    } else if (event.ctrlKey && event.key === 'i' && (currentStep.value > 0 && currentStep.value < 3)) {
        showPassword.value = !showPassword.value
    }
}

// handles if the user clicks somewhere
function handleClick() {
    document.getElementById('cmd-input').focus();
}

// TODO auth
function auth() {
    if (cmdinput.value == "Y") {
        if (route.path === "/login"){
            login()
        } else {
            signup()
        }
    } else {
        location.reload()
    }
}

function errorMessage() {
    credentials.value = []
    currentStep.value = 0

    executedCommands.value += inputName.value + "\n" + "> " + cmdinput.value + "\n" + "No such account exists - try again"

    inputName.value = "Email:"
    cmdinput.value = ""
}

async function login() {
    const { data, error } = await supabase.auth.signInWithPassword({
        email: credentials.value[0],
        password: credentials.value[1]
    })
    if (error) {
        switch (error.message) {
            case "Invalid login credentials":
                errorMessage()
                break
        }
    } else {
        router.push('/')
        location.reload()
    }
}

async function signup() {
    const { data, error } = await supabase.auth.signUp({
        email: credentials.value[0],
        password: credentials.value[1]
    })
    if (error) {
        console.log(error)
    } else {
        router.push('/')
    }
}

async function loginWithGoogle(){
    supabase.auth.signInWithOAuth({
        provider: 'google',
    })
}
</script>