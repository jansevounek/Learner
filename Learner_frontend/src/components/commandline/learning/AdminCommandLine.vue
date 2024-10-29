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
import { supabase } from '@/supabase/init.js'

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
        case "Home":
        case "go 1":
            router.push('/')
            break
        case "Logout":
        case "go 6":
            logout()
            break
        case "Lets learn":
        case "go 7":
            router.push('/learning/user')
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
        //done
        case command.startsWith("team create"):
            createTeam(command);
            return true
        //done
        case command === "team ps":
            getTeams();
            return true
        //done
        case command.startsWith("team delete"):
            deleteTeam(command);
            return true
        //done
        case command.startsWith("lesson create"):
            createLesson();
            return true
        case command.startsWith("lesson cancel"):
            cancelLesson();
            return true
        case command.startsWith("lesson ps"):
            getLessons();
            return true
        case command.startsWith("lesson solutions"):
            seeSolutions();
            return true
    }
    return false;
}

// done
async function createTeam(c) {
    let name = c.replace("team create ", "")

    if (name) {
        const { data: { user } } = await supabase.auth.getUser();
        const apiurl = import.meta.env.VITE_API_URL
        const response = await fetch(apiurl + "/teams/admin/create", {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
                user_id: user.id,
                team_name: name,
            })
        });

        const data = await response.json()
        commandOutput(data.msg)
    }
}


// done
async function getTeams() {
    let extra = await getUserExtra()

    if (extra) {
        const { data, error } = await supabase
            .from('team')
            .select('*')
            .eq('creator_id', extra.id);
        if (error) {
            commandOutput("User information incomplete - contact support")
            return
        }

        printTeams(data)
    } else {
        commandOutput("User information incomplete - contact support")
        return
    }
}

function printTeams(data) {
    let output = "user@linuxlearning:~$ " + cmdinput.value + "\n\n"

    if (data.length == 0){
        executedCommands.value += "user@linuxlearning:~$ " + cmdinput.value + "\n"
                                 + "No teams found \n"
    } else {
        for (let i = 0; i < data.length; i++) {
            output += i + 1 + ".\n name: " + data[i].name + "\n"
                + "team code: " + data[i].team_code + "\n\n"
        }
        executedCommands.value += output
    }

    cmdinput.value = ""
}


async function deleteTeam(c) {
    let name = c.replace("team delete ", "")

    if (name) {
        const { data: { user } } = await supabase.auth.getUser();
        const apiurl = import.meta.env.VITE_API_URL
        const response = await fetch(apiurl + "/teams/admin/delete", {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
                user_id: user.id,
                team_name: name,
            })
        });

        const data = await response.json()
        commandOutput(data.msg)
    }
}

async function createLesson() {
    let extra = await getUserExtra()

    if (extra) {
        const { data, error } = await supabase
            .from('limitations')
            .select('lesson_limit, lessons, teams')
            .eq('extra_id', extra.id);
        if (error) {
            commandOutput("User information incomplete - contact support")
            return
        }

        if (data.length > 1) {
            commandOutput("User information error - contact support")
            return
        } else {
            if (data[0].teams > 0) {
                if (data[0].lesson_limit > data[0].lessons) {
                    router.push("/learning/create-lesson")
                } else {
                    commandOutput("You have reached the maximum of lessons you can create")
                    return
                }
            } else {
                commandOutput("You need to have at least one team for which to create a lesson")
                return
            }
        }
    } else {
        commandOutput("User information incomplete - contact support")
        return
    }
}

function cancelLesson() {

}

async function getLessons() {
    let extra = await getUserExtra()

    if (extra) {
        const { data, error } = await supabase
            .from("lesson")
            .select("*")
            .eq('creator_id', extra.id)
        if (error) {
            commandOutput("User information incomplete - contact support")
            return
        }

        printLessons(data)
    } else {
        commandOutput("User information incomplete - contact support")
        return
    }
}

async function printLessons(lesson) {

    let output = "user@linuxlearning:~$ " + cmdinput.value + "\n\n"

    if (lesson.length == 0){
        executedCommands.value += "user@linuxlearning:~$ " + cmdinput.value + "\n"
                                 + "No lessons found \n"
    } else {
        for (let i = 0; i < lesson.length; i++) {
            const { data, error } = await supabase
                .from("team")
                .select("*")
                .eq('id', lesson[i].team_id)
            if (error) {
                break
            }
            output += i + 1 + ".\n name: " + lesson[i].name + "\n"
                + "start: " + lesson[i].start_time + "\n"
                + "end: " + lesson[i].end_time + "\n"
                + "team: \n" 
                + "a) name: " + data[0].name + "\n"
                + "b) code: " + data[0].team_code + "\n"
                + "settings: \n"
                + "a) load allowed: " + lesson[i].settings["load"] + "%\n"
                + "b) network needed: " + lesson[i].settings["network"] + "\n"
                + "c) sudo needed: " + lesson[i].settings["sudo"] + "\n\n"
        }
        executedCommands.value += output
    }

    cmdinput.value = ""
}

function seeSolutions() {

}

async function getUser() {
    const { data: { user } } = await supabase.auth.getUser();
    if (user) {
        return user;
    } else {
        return false;
    }
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

async function getLimitations() {
    const extra = await getUserExtra();
    if (extra) {
        const { data, error } = await supabase
            .from('limitations')
            .select('*')
            .eq('extra_id', extra.id);
        if (error) {
            console.log(error)
            return false
        }
        if (data) {
            return data[0]
        } else {
            return false
        }
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