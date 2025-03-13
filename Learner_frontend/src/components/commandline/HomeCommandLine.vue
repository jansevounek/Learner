<template>
    <div class="cmd-line-container">
        <div class="cmd-output-container">
            {{ executedCommands }}
        </div>
        <div class="cmd-line-input-container">
            <h1 id="inputTitle">user@linuxlearning:~$</h1>
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
import { getUser } from '@/supabase/getFunctions.js'
import { loadStripe } from '@stripe/stripe-js';

// router import a setup
import { useRouter } from 'vue-router'
const router = useRouter()

const input = ref(null)

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY)

const cmdinput = ref('');
let executedCommands = ref('')
const executedList = ref([])
let executedIndex = ref(0)

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

// function that checks all the commands
function executeCommand() {
    if (cmdinput.value !== ''){
        executedList.value.push(cmdinput.value)
        executedIndex.value = executedList.value.length
    }
    let command = cmdinput.value
    switch (command) {

        // Essentials
        case "clear":
            clearLines()
            break
        case "help":
            getHelp()
            break
        case "buy premium":
            createCheckout()
            break
        case "mode":
            changeMode()
            break

        // Navbar top
        case "Admin":
        case "go 8":
            router.push('/learning/admin')
            break
        case "Lets Learn":
        case "go 7":
            router.push('/learning/user')
            break
        case "Logout":
        case "go 6":
            logout()
            break
        case "Forgot Password?":
        case "go 5":
            router.push('/resetpassword')
            break
        case "About us":
        case "go 4":
            router.push('/')
            output = getAboutUs()
            break
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

        // Navbar Bottom
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
            commandError()
    }
}

// clears all the lines of output
function clearLines() {
    executedCommands.value = ''
    cmdinput.value = ''
}

// returns a string containing help info
function getHelp() {
    commandOutput('\nTo navigate and use this application you can use these commands: \n' +
            '\n' +
            ' Essential commands: \n' +
            ' "help" - this command displayed this info about how to use the app \n' +
            ' "go " + (number / The name written below the number "Home", etc.) - this command lets you navigate throw our app (by chosing the number written above the place you want to go in the navigation bar) \n' +
            ' "clear" - using this command simply clears the lines that you writing your commands created \n \n' +
            ' Extra commands: \n' +
            ' "Github" - This command takes you to the github page of this web application \n' +
            ' "Socials" - This command takes you to the social pages of this application \n' +
            ' "License" - This command displays the MIT license under which the application is published \n' +
            ' "buy premium" - Redirects you to a site where you can buy a premium account - note: if you have bought the premium account and you didnt get the upgrade - contact support \n' +
            '\n' +
            'further information about other parts of the app will be provided as soon as you get there - use the magic command "help" again ;) \n' + 
            '\n' +
            "You will be able to learn and use the app as soon as you sign up/log in. \n")
}

// returns a string containing info about the company
function getAboutUs() {
    commandOutput('\nFIRST OF ALL: This web application was created just as a project needed for Graduation.' + '\n' +
                    "I hope you enjoy what the application has to offer and its (in the creators humble opinion :)) unique style \n" +
                    "There is really no real real reason for deployment, however if you are reading this you are either reading this code or it has been deployed. \n" + 
                    "Never the less i hope it is usefull to someone (even as a source of code). \n" +
                    "All of the source code is openly availible at https://github.com/jansevounek/Learner with the complete documentation and if you want to try and \n" + 
                    "set it up for yourself (don't :)) there is a guide available at https://jansevounek.github.io/Learner/ \n" +
                    "Any kind of feedback is greatly appreciated! \n"
    )
}

function commandOutput(output) {
    executedCommands.value += "user@linuxlearning:~$ " + cmdinput.value + "\n" +
                        output + "\n"
    cmdinput.value = ""
}

function commandError() {
    let input = cmdinput.value
    if (input === "") {
        executedCommands.value += "user@linuxlearning:~$ \n"
        cmdinput.value = ""
    } else {
        executedCommands.value += "user@linuxlearning:~$ " + cmdinput.value + "\n" + 'Command: "' + cmdinput.value + '" is not recognised as a command that can be used \n'
        cmdinput.value = ""
    }
}

// handels the "ctrl + c" shortcut
function handleKeyDown(event) {
    if (event.ctrlKey && event.key === 'l') {
        event.preventDefault(); // Prevent the default action (e.g., focusing the browser's address bar)
        clearLines()    
    } else if (event.key === 'ArrowUp') {
        if((executedIndex.value - 1) >= 0) {
            executedIndex.value--
            changeCommand()
        }
    } else if (event.key === 'ArrowDown') {
        if((executedIndex.value + 1) <= executedList.value.length) {
            executedIndex.value++
            changeCommand()
        }
    }
}

function changeCommand(){
    cmdinput.value = executedList.value[executedIndex.value]
}

function changeMode() {
    console.log(localStorage.theme)
    // taken from https://dev.to/dirheimerb/implementing-custom-dark-mode-with-tailwind-css-a-complete-guide-3n0h
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.remove('dark');
        localStorage.theme = "light"
        commandOutput("Dark mode enabled")
    } else {
        document.documentElement.classList.add('dark');
        localStorage.theme = "dark"
        commandOutput("Light mode enabled")
    }
}

// handles if the user clicks somewhere
function handleClick() {
    document.getElementById('cmd-input').focus();
}

async function createCheckout() {
    const user = await getUser()
    if (user.premium == false) {
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
        } else {
            commandOutput("There has been a problem redirecting you to the payment page - contact support")
        }
    } else {
        commandOutput("You already have a premium account")
    }
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
</script>