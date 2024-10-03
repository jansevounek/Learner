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
    //TODO remove these
    switch (true) {
        case command == "container":
            printContainerHelp()
            return true
        
        // done
        case command.startsWith("container ps"):
            printContainers(command)
            return true

        // done
        case command.startsWith("container create "):
            createContainer(command)
            return true

        // done
        case command.startsWith("container delete "):
            deleteContainer(command)
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

async function printContainers(c) {
    // taken from https://www.w3schools.com/js/js_errors.asp

    let command = c.replace("container ps", "")
    let showPassword = false
    if (command) {
        if (command === " -p") {
            showPassword = true
        } else {
            commandError()
            return 0
        }
    }

    let containers = await fetchUsersContainers()

    let output = "user@linuxlearning:~$ " + cmdinput.value + "\n\n"

    for (let i = 0; i < containers.length; i++){
        output += i + 1 + ".\n name: " + containers[i].name + "\n"
            + "login: " + containers[i].login + "\n"
        // taken from https://stackoverflow.com/questions/1789945/how-to-check-whether-a-string-contains-a-substring-in-javascript/
        if (showPassword) {
            output += "password: " + containers[i].pass + "\n"
        }
        if (containers[i].sudo) {
            output += "sudo: True \n"
        } else {
            output += "sudo: False \n"
        }
        output += "\n"
    }

    executedCommands.value += output

    cmdinput.value = ""
}

async function createContainer(input) {
    let name = input.replace("container create ", "")
    if (name) {
        const user = await getUser()
        const apiurl = import.meta.env.VITE_API_URL
        const response = await fetch(apiurl + "/create/container", {
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
        printContainerOutputs(data)
    }
}

async function deleteContainer(input) {
    let name = input.replace("container delete ", "")
    if (name) {
        const user = await getUser()
        const apiurl = import.meta.env.VITE_API_URL
        const response = await fetch(apiurl + "/delete/container", {
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
        printContainerOutputs(data)
    }
}

function startContainer() {
    console.log("Start")
}

function stopContainer() {
    console.log("stop")
}

function attachContainer() {
    console.log("attach")
}

function printContainerOutputs(data){
    executedCommands.value += "user@linuxlearning:~$ " + cmdinput.value + "\n" +
                        data.msg + "\n"
    // TODO uncomment cmdinput.value = ""
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

async function fetchUsersContainers() {
    const user = await getUser()

    let extra_id = 0

    const { data, error } = await supabase
        .from('user')
        .select('id')
        .eq('user_id', user.id);
    if (error) {
        throw error
    }
    extra_id = data[0].id

    if (extra_id) {
        const { data, error } = await supabase
            .from('container')
            .select('*')
            .eq('extra_id', extra_id);
        if (error) {
            throw error
        }
        return data
    } else {
        throw "Failed to fetch users extra - no extra_id"
    }
}

function changeCommand() {
    cmdinput.value = executedList.value[executedIndex.value]
}
// handles if the user clicks somewhere
function handleClick() {
    document.getElementById('cmd-input').focus();
}
</script>