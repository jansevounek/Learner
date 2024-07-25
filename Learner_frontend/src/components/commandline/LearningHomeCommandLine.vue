<template>
    <div class="cmd-line-container" v-if="!preparingContainer">
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
    <div class="cmd-loading-bar" v-if="preparingContainer">
        <h1>{{ loadingName }}</h1>
        {{ loadingBar }}
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
let preparingContainer = ref(false)
let loadingBar = ref('[---------------------------------]')
let loadingName = ref('Loading...')

// mounting handlers for shortcuts
onMounted(() => {
    window.addEventListener('keydown', handleKeyDown);
    document.addEventListener('click', handleClick);
})

onUnmounted(() => {
    window.removeEventListener('keydown', handleKeyDown);
    document.removeEventListener('click', handleClick);
})

function executeCommand() {
    switch(cmdinput.value) {
        case "Home":
        case "navbar 1":
            router.push('/')
            break
        case "Logout":
        case "navbar 6":
            logout()
            router.push('/')
            break

        case "lections":
        case "Lections":
            router.push('/learning/lections')
            break

        // practice stuff
        case "practice":
        case "Practice":
            preparePractice()
            break
        case "credentials":
        case "Credentials":
            printCredntials()
            break
        case "attach":
        case "Attach":
            attach()
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

        // Essentials
        case "clear":
            clearLines()
            break
        case "help":
            getHelp()
            break
        
        default:
            commandError()
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

// clears all the lines of output
function clearLines() {
    executedCommands.value = ''
    cmdinput.value = ''
}

function getHelp() {
    executedCommands.value += "user@linuxlearning:~$ " + cmdinput.value + "\n" +
                                'TODO help - command "help"' + "\n \n"
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

async function preparePractice() {
    preparingContainer.value = true

    // taken from https://stackoverflow.com/questions/951021/what-is-the-javascript-version-of-sleep
    await new Promise(r => setTimeout(r, 500));
    loadingBar.value = '[############---------------------]'

    loadingName.value = 'Preparing enviroment'
    const status = await startContainer()
    loadingBar.value = '[######################-----------]'

    loadingName.value = 'You will be redirected in a moment'
    await new Promise(r => setTimeout(r, 500));
    loadingBar.value = '[#################################]'
    await new Promise(r => setTimeout(r, 500));

    preparingContainer.value = false
    if (status == "started") {
        executedCommands.value += "user@linuxlearning:~$ " + cmdinput.value + "\n" + 
                                'Your container is prepared and running type the command "credentials" to see your login credentials for it and to use it type "attach"\n \n'
    } else if (status == "already_started") {
        executedCommands.value += "user@linuxlearning:~$ " + cmdinput.value + "\n" + 
                                'Your container was already prepared and running (you do not need to retype this command if it is already started) type the command "credentials" to see your login credentials for it and to use it type "attach"\n \n'
    } else {
        executedCommands.value += "user@linuxlearning:~$ " + cmdinput.value + "\n" + 
                                'There was a problem starting your container - please contact support\n'  + "\n"
    }
    cmdinput.value = ''
}

async function startContainer() {
    const { data: { user } } = await supabase.auth.getUser()

    const response = await fetch("http://127.0.0.1:5000/start-container", {
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
    return responseData.status
}

async function printCredntials() {
    const { data: { user } } = await supabase.auth.getUser()
    const { data, error } = await supabase
        .from('user_extra')
        .select('*')
        .eq('user_id', user.id)
        .single();
    
    executedCommands.value += "user@linuxlearning:~$ " + cmdinput.value + "\n" +
                        "Login: " + data.container_login + "\n" +
                        "Password: " + data.container_password + "\n" +
                        "Do not show this info to anyone" + "\n \n"
    cmdinput.value = ''
}

async function attach() {
    const { data: { user } } = await supabase.auth.getUser()
    const { data, error } = await supabase
        .from('user_extra')
        .select('*')
        .eq('user_id', user.id)
        .single();

    const port = 8000 + data.id
    window.location.replace("http://127.0.0.1:" + port + "/");
}

// handels the "ctrl + c" shortcut
function handleKeyDown(event) {
    if (event.ctrlKey && event.key === 'l') {
        event.preventDefault(); // Prevent the default action (e.g., focusing the browser's address bar)
        clearLines()    
    } else if (event.ctrlKey && event.key === 'c') {
        location.reload()
    }
}

// handles if the user clicks somewhere
function handleClick() {
    document.getElementById('cmd-input').focus();
}
</script>