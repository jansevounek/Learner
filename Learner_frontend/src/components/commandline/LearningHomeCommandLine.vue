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
        
        case "Lections":
            router.push('/learning/lections')
            break

        case "Practice":
            window.location.replace("http://127.0.0.1:4200");
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

// handels the "ctrl + c" shortcut
function handleKeyDown(event) {
    if (event.ctrlKey && event.key === 'l') {
        event.preventDefault(); // Prevent the default action (e.g., focusing the browser's address bar)
        clearLines()    
    }
}

// handles if the user clicks somewhere
function handleClick() {
    document.getElementById('cmd-input').focus();
}
</script>