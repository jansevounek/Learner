<template>
    <div class="cmd-line-container">
        <div class="cmd-output-container">
            {{ executedCommands }}
        </div>
        <div class="cmd-line-input-container">
            <h1 id="inputTitle">user@linuxlearning:~$</h1>
            <input type="text" class="cmd-input" id="cmd-input" v-on:keyup.enter="executeCommand"  v-model="cmdinput" autofocus>
        </div>
        <button class="cmd-input-mobile-btn" @click="executeCommand">
            Execute
        </button>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { supabase } from '../../supabase/init.js'

// router import a setup
import { useRouter } from 'vue-router'
const router = useRouter()

const cmdinput = ref('');
let executedCommands = ref('')
const executedList = ref([])
let executedIndex = ref(0)

// mounting handlers for shortcuts
onMounted(() => {
    checkUser()
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
    let output = ''
    let command = cmdinput.value
    switch (command) {

        // Essentials
        case "clear":
            output = clearLines()
            break
        case "help":
            output = getHelp()
            break

        // Navbar top
        case "Lets Learn":
        case "navbar 7":
            router.push('/learning/homepage')
            break
        case "Logout":
        case "navbar 6":
            logout()
            break
        case "Forgot Password?":
        case "navbar 5":
            router.push('/resetpassword')
            break
        case "About us":
        case "navbar 4":
            router.push('/')
            output = getAboutUs()
            break
        case "Signup":
        case "navbar 3":
            router.push('/signup')
            break
        case "Login":
        case "navbar 2":
            router.push('/login')
            break
        case "Home":
        case "navbar 1":
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
            router.push('/getpremium')
            break

        // other possibilities
        case "":
            break
        default:
            output = 'Command: "' + command + '" is not recognised as a command that can be used'
    }
    // solving the graphical output
    if (output === 'none') {
        executedCommands.value = ''
        cmdinput.value = ''
    } else if (output === '') {
        executedCommands.value += 'user@linuxlearning:~$ \n'
        cmdinput.value = ''
    } else {
        executedCommands.value += 'user@linuxlearning:~$ ' + command + '\n' + output + '\n'
        cmdinput.value = ''
    }
}

// clears all the lines of output
function clearLines() {
    executedCommands.value = ''
    cmdinput.value = ''
    return 'none'
}

// returns a string containing help info
function getHelp() {
    return 'To navigate and use this application you can use these commands: \n' +
            '\n' +
            ' "help" - this command displayed this info about how to use the app \n' +
            ' ("navbar " + number) / (The name written below the number "Home", etc.) - this command lets you navigate throw our app (by chosing the number written above the place you want to go in the navigation bar) \n' +
            ' "clear" - using this command simply clears the lines that you writing your commands created \n' +
            '\n' +
            'further information about other parts of the app will be provided as soon as you get there :) \n' + 
            '\n' +
            "You will be able to learn and use the app as soon as you sign up/log in. \n"
}

// returns a string containing info about the company
function getAboutUs() {
    return 'Here the user will get giberish about my project' + '\n'
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

// handles if the user clicks somewhere
function handleClick() {
    document.getElementById('cmd-input').focus();
}

async function checkUser() {
    const { data: { user } } = await supabase.auth.getUser()

    if (user) {
        if(await extraExists(user) === false) {
            setUpUser(user)
        }
    }
}

async function extraExists(user) {
    const { data, error } = await supabase
        .from('user_extra')
        .select('*')
        .eq('user_id', user.id);
    
    if(error) {
        console.log(error)
    }
    if(data) {
        if(data.length == 0) {
            return false
        } else {
            return true
        }
    }

    return true
}

async function setUpUser(user) {
    const apiurl = import.meta.env.VITE_API_URL
    const response = await fetch(apiurl + "/create-container", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(user.id),
    });
    
    if (!response.ok) {
      throw new Error('Network response was not ok ' + response.statusText);
    }
    
    const responseData = await response.json();
    console.log(responseData);
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