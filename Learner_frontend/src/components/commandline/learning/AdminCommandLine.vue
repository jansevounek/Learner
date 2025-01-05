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
import { getUser, getUserExtra, getTeam, getLesson } from '@/supabase/getFunctions.js'

// router import a setup
import { useRouter } from 'vue-router'
import { textSync } from 'figlet'
const router = useRouter()

const input = ref(null)

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
            router.push('/')
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
        case "fent":
            test()
            console.log("fent")
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

async function test() {
    await supabase.from('lesson').update({task :"fent"}).eq("id", 50);
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
            printTeams();
            return true
        //done
        case command.startsWith("team delete"):
            deleteTeam(command);
            return true
        //done
        case command === "lesson create":
            createLesson();
            return true
        //done
        case command.startsWith("lesson cancel "):
            cancelLesson(command);
            return true
        //done
        case command.startsWith("lesson ps"):
            printLessons();
            return true
        case command.startsWith("lesson solution "):
            seeSolutions(command);
            return true
    }
    return false;
}

// done
async function createTeam(c) {
    let name = c.replace("team create ", "")

    if (name) {
        const user = await getUser();
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
    } else {
        commandOutput("No name provided - please provide a name")
    }
}


// done
async function printTeams() {
    const data = await getUserExtra()
    const extra = data[0]
    const teams = await getTeam({ creator_id : extra.id })

    let output = "user@linuxlearning:~$ " + cmdinput.value + "\n\n"

    if (teams.length == 0){
        executedCommands.value += "user@linuxlearning:~$ " + cmdinput.value + "\n"
                                 + "No teams found \n"
    } else {
        for (let i = 0; i < teams.length; i++) {
            output += i + 1 + '.\n name: "' + teams[i].name + '"\n'
                + 'team code: "' + teams[i].team_code + '"\n\n'
        }
        executedCommands.value += output
    }

    cmdinput.value = ""
}


async function deleteTeam(c) {
    let name = c.replace("team delete ", "")

    if (name) {
        const user = await getUser();
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
    } else {
        commandOutput("No name provided - please provide a name")
    }
}

async function createLesson() {
    const data = await getUserExtra()
    const extra = data[0]

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

async function cancelLesson(c) {
    let name = c.replace("lesson cancel ", "")

    if (name) {
        const user = await getUser();
        const apiurl = import.meta.env.VITE_API_URL
        const response = await fetch(apiurl + "/lessons/admin/cancel", {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
                user_id: user.id,
                lesson_name: name,
            })
        });

        const data = await response.json()
        commandOutput(data.msg)
    } else {
        commandOutput("No name provided - please provide a name")
    }
}

async function printLessons() {
    const lessons = await getLesson()
    
    let output = "user@linuxlearning:~$ " + cmdinput.value + "\n\n"

    if (lessons.length == 0) {
        executedCommands.value += "user@linuxlearning:~$ " + cmdinput.value + "\n"
                                 + "No lessons found \n"
    } else {
        for (let i = 0; i < lessons.length; i++) {
            const team = await getTeam({ id : lessons[i].team_id })

            output += i + 1 + '.\n name: "' + lessons[i].name + '"\n'
                + 'start: "' + lessons[i].start_time + '"\n'
                + 'end: "' + lessons[i].end_time + '"\n'
                + 'team: \n' 
                + 'a) name: "' + team[0].name + '"\n'
                + 'b) code: "' + team[0].team_code + '"\n'
                + 'settings: \n'
                + 'a) network load allowed: ' + lessons[i].settings['network_load'] + '%\n'
                + 'b) cpu load allowed: ' + lessons[i].settings['cpu_load'] + '%\n'
                + 'c) network needed: ' + lessons[i].settings['network'] + '\n'
                + 'd) sudo needed: ' + lessons[i].settings['sudo'] + '\n'
            
            let todaysTime = new Date();
            let endTime = new Date(lessons[i].end_time);

            if (todaysTime > endTime) {
                output += "lesson ended: true \n\n"
            } else {
                output += "lesson ended: false \n\n"
            }
        }
        executedCommands.value += output
    }
    cmdinput.value = ""
}

// TODO for testing keep without time check - then change
async function seeSolutions(c) {
    let name = c.replace("lesson solution ", "")

    if (name) {
        const lesson = await getLesson({ name : name })

        router.push("/learning/solutions/" + lesson[0].id)
    } else {
        commandOutput("No name provided - please provide a name")
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