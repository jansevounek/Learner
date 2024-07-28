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
                                'To use the learning part of this application use commands: \n' + '\n' +
                                ' "Lections" - this command lets you choose between many lections we provide \n' +
                                ' "Practice" - this command lets you start your practice container (use this command visely as you only have a limited time daily to use it) \n \n' +
                                'You can additionally use all the other commands from the homapage \n \n'
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
    const { data: { user } } = await supabase.auth.getUser()
    const { data, error } = await supabase
        .from('user_extra')
        .select('container_used')
        .eq('user_id', user.id);

    console.log(data[0].container_used)

    preparingContainer.value = true

    // taken from https://stackoverflow.com/questions/951021/what-is-the-javascript-version-of-sleep
    await new Promise(r => setTimeout(r, 500));
    loadingBar.value = '[############---------------------]'

    loadingName.value = 'Preparing enviroment'

    let status = 'used'
    if (!data[0].container_used) {
        status = await startContainer(user)
        const { error } = await supabase
            .from("user_extra")
            .update({"container_used" : true})
            .eq("user_id", user.id)
        if (error) {
            console.log('error: ' + error)
        }
        loadingBar.value = '[######################-----------]'
    }

    loadingName.value = 'Your learning command line will be prepared soon'
    await new Promise(r => setTimeout(r, 500));
    loadingBar.value = '[#################################]'
    await new Promise(r => setTimeout(r, 500));

    preparingContainer.value = false
    if (status == "started") {
        executedCommands.value += "user@linuxlearning:~$ " + cmdinput.value + "\n" + 
                                'Your container is prepared and running type the command "credentials" to see your login credentials for it and to use it type "attach"\n \n' +
                                'Your container will be automatically turned off when 30 minutes pass (you have only 30 minutes of learning time daily) \n \n'
    } else if (status == "already_started") {
        executedCommands.value += "user@linuxlearning:~$ " + cmdinput.value + "\n" + 
                                'Your container was already prepared and running (you do not need to retype this command if it is already started) type the command "credentials" to see your login credentials for it and to use it type "attach"\n \n' +
                                'Your container will be automatically turned off when 30 minutes pass (you have only 30 minutes of learning time daily) \n \n'
    } else if (status == "used") {
        executedCommands.value += "user@linuxlearning:~$ " + cmdinput.value + "\n" + 
                                'You already used the runtime of your container today\n \n' +
                                'You will have your runtime back tomorrow \n \n'
    } else {
        executedCommands.value += "user@linuxlearning:~$ " + cmdinput.value + "\n" + 
                                'There was a problem starting your container - please contact support\n'  + "\n"
    }
    cmdinput.value = ''
}

async function startContainer(user) {

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

function changeCommand(){
    cmdinput.value = executedList.value[executedIndex.value]
}
// handles if the user clicks somewhere
function handleClick() {
    document.getElementById('cmd-input').focus();
}
</script>