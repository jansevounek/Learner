<template>
    <div class="cmd-line-container">
        <div class="cmd-output-container">
            {{ executedCommands }}
        </div>
        <div class="cmd-arrow-input" v-for="(command, index) in commands" :key="index">
            <div v-if="currentIndex === index">
                <p class="cmd-arrow-name">Type in "{{ command }}"</p>
                <div class="cmd-line-input-container">
                    <h1>></h1>
                    <input class="cmd-input" id="cmd-input" v-model="cmdinput" autofocus v-on:keyup.enter="executeCommand" >
                </div>
            </div>
        </div>
        <div class="cmd-arrow-input" v-if="currentIndex === maxLength">
            <p class="cmd-arrow-name">Type in "continue"</p>
            <div class="cmd-line-input-container">
                <h1>></h1>
                <input class="cmd-input" id="cmd-input" v-model="cmdinput" autofocus v-on:keyup.enter="executeCommand" >
            </div>
        </div>
        <button class="cmd-input-mobile-btn" @click="executeCommand">
            Execute
        </button>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useRoute } from 'vue-router'
import { supabase } from '../../supabase/init.js'

const route = useRoute()
const router = useRouter()
const lection = ref()
const maxLength = ref()
const commands = ref()

let cmdinput = ref('')
let executedCommands = ref('')
let currentIndex = ref(0)

onMounted(() => {
    getLesson()
    window.addEventListener('keydown', handleKeyDown);
    document.addEventListener('click', handleClick);
})

onUnmounted(() => {
    window.removeEventListener('keydown', handleKeyDown);
    document.removeEventListener('click', handleClick);
})

function executeCommand() {
    switch(cmdinput.value) {
        case "clear":
            clearLines()
            break
        case "help":
            getHelp()
            break

        case "Lets Learn":
        case "go 7":
            router.push('/learning/homepage')
            break
        case "Home":
        case "go 1":
            router.push('/')
            break
        case "Logout":
        case "go 6":
            logout()
            router.push('/')
            break
        
        case "continue":
            router.push('/')
            break
        case "":
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
            checkCommand()
            break
    }
}

function checkCommand() {
    if (cmdinput.value === commands.value[currentIndex.value]) {
        console.log("now")
        executedCommands.value += 'Type in "' + commands.value[currentIndex.value] + '"\n > ' + cmdinput.value + '\n' + lection.value["command_definitions"][currentIndex.value] +'\n \n'
        cmdinput.value = ''
        currentIndex.value++;
    } else {
        executedCommands.value += 'Type in "' + commands.value[currentIndex.value] + '"\n > ' + cmdinput.value + '\n Command: "' + cmdinput.value + '" is not a command \n \n'
        cmdinput.value = ""
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

async function getLesson() {
    const { data, error } = await supabase
        .from("lections")
        .select("*")
        .eq("id", route.params.id)
    
    if(error){
        router.push('/learning/lections')
    }

    if (data.length == 1) {
        lection.value = await data[0]
        console.log(lection.value)
        maxLength.value = lection.value["commands"].length
        console.log(maxLength.value)
        commands.value = lection.value["commands"]
    } else {
        router.push('/learning/lections')
    }
}

// clears all the lines of output
function clearLines() {
    executedCommands.value = ''
    cmdinput.value = ''
}

function getHelp() {
    executedCommands.value = ''
    cmdinput.value = ''
    executedCommands.value += "Help: \n" +
                                "TODO" +
                                "\n" +
                                '"continue" to skip' +
                                "\n" +
                                "\n"
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