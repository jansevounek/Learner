<template>
    <div class="cmd-line-container" v-if="!loading">
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
    <div class="cmd-loading-bar" v-if="loading">
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
let loading = ref(false)
let loadingBar = ref('[---------------------------------]')
let loadingName = ref('Loading...')
const executedList = ref([])
let executedIndex = ref(0)

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
    if (cmdinput.value !== ''){
        executedList.value.push(cmdinput.value)
        executedIndex.value = executedList.value.length
    }
    switch(cmdinput.value) {
        case "Home":
        case "go 1":
            router.push('/')
            break
        case "Logout":
        case "go 6":
            logout()
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

        // Essentials
        case "clear":
            clearLines()
            break
        case "help":
            getHelp()
            break
        
        default:
            if (!containerCommands()) {
                commandError()
            }
    }
}

function containerCommands() {
    // taken from https://stackoverflow.com/questions/63002735/can-you-use-functions-within-a-switch-case-in-javascript
    const command = cmdinput.value
    switch (true) {
        case command == "container":
            printContainerHelp()
            return true

        case command == "container credentials":
            printCredentials()
            return true
        
        case command == "container ps":
            printContainers()
            return true

        case command.startsWith("container create "):
            createContainer(cmdinput.value)
            return true
        
        case command.startsWith("container start "):
            startContainer()
            return true

        case command.startsWith("container stop "):
            stopContainer()
            return true

        case command.startsWith("container attach "):
            attachContainer()
            return true
    }
    return false
}

function printContainerHelp(){
    executedCommands.value += "user@linuxlearning:~$ " + cmdinput.value + "\n" +
                        "TODO"
    cmdinput.value = ""
}

function printContainers() {
    console.log("TODO")
}

function startContainer() {
    console.log("Start")
}

async function createContainer(input) {
    let name = input.replace("container create ", "")
    if (name) {
        const user = await getUser()
        const apiurl = import.meta.env.VITE_API_URL
        const response = await fetch(apiurl + "/physical/create-container", {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
                user_id: user.id,
                container_name: name
            })
        });

        const data = await response.json()
        console.log(data)
    }
}

function stopContainer() {
    console.log("stop")
}

function attachContainer() {
    console.log("attach")
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
                                'Add help please: \n'          
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

async function printCredentials() {
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

// handels the "ctrl + c" shortcut
function handleKeyDown(event) {
    if (event.ctrlKey && event.key === 'l') {
        event.preventDefault(); // Prevent the default action (e.g., focusing the browser's address bar)
        clearLines()    
    } else if (event.ctrlKey && event.key === 'c') {
        location.reload()
    }  else if (event.key === 'ArrowUp') {
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

async function getUser() {
    const { data: { user } } = await supabase.auth.getUser()
    return user
}

function changeCommand() {
    cmdinput.value = executedList.value[executedIndex.value]
}
// handles if the user clicks somewhere
function handleClick() {
    document.getElementById('cmd-input').focus();
}
</script>