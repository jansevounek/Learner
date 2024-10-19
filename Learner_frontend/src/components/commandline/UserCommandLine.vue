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
    window.addEventListener('keydown', handleKeyDown);
    document.addEventListener('click', handleClick);
})

onUnmounted(() => {
    window.removeEventListener('keydown', handleKeyDown);
    document.removeEventListener('click', handleClick);
})

function executeCommand() {
    switch(cmdinput.value) {

        // navbar commands
        case "Admin":
        case "go 8":
            router.push('/learning/admin')
            break
        case "Home":
        case "go 1":
            router.push('/learning/admin')
            break
        case "Logout":
        case "go 6":
            router.push('/learning/admin')
            break

        // general commands
        case "help":
            getHelp()
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

        default:
            if (!adminCommands()) {
                commandError()
            }
    }
}

function adminCommands() {
    const command = cmdinput.value

    switch(true) {
        // done
        case command.startsWith("team join"):
            joinTeam(command);
            return true
        case command.startsWith("team leave"):
            leaveTeam(command);
            return true
        case command == "team ps":
            getTeams();
            return true
        //TODO do the lessons
    }
    return false;
}

//done
async function joinTeam(c) {
    let teamCode = c.replace("team join ", "")
    let extra = await getUserExtra();

    if (extra) {
        const { data, error } = await supabase.from("team").select("id, name").eq('team_code', teamCode )
        
        if (error) {
            commandOutput("An error occured while accessing this team - contact support")
            return
        }
        if (data) {
            // taken from https://stackoverflow.com/questions/237104/how-do-i-check-if-an-array-includes-a-value-in-javascript
            let arr = extra.teams
            if (!arr) {
                arr = [data[0].id]
            } else {
                if (arr.includes(data[0].id)) {
                    commandOutput('You already are a part of team "' + data[0].name + '"')
                    return
                }
                arr.push(data[0].id)
            }
            const { error } = await supabase.from("user").update({ teams: arr }).eq("id", extra.id)

            if (error) {
                console.log(error)
                commandOutput("An error occured while adding you to the team - contact support")
                return
            }

            commandOutput('You successfully joined team "' + data[0].name + '"')
        } else {
            commandOutput('No team with code "' + teamCode + '" found')
            return
        }
    } else {
        commandOutput("User profile incpomplete - contact support")
        return
    }
}

async function leaveTeam(c) {
    let teamCode = c.replace("team leave ", "")
}

async function getTeams() {
    
}

async function getUserExtra() {
    const { data: { user } } = await supabase.auth.getUser();
    const { data, error } = await supabase
        .from('user')
        .select('*')
        .eq('user_id', user.id);
    if (error) {
        return false
    }
    if (data) {
        return data[0]
    } else {
        return false
    }
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

function clearLines() {
    executedCommands.value = ''
    cmdinput.value = ''
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

function handleClick() {
    document.getElementById('cmd-input').focus();
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