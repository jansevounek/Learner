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

// router import a setup
import { useRouter } from 'vue-router'
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
        case "Admin":
        case "go 8":
            router.push('/learning/admin')
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
        // done
        case command.startsWith("team leave"):
            leaveTeam(command);
            return true
        // done
        case command == "team ps":
            getTeams();
            return true
        // done
        case command == "lesson ps":
            getLessons();
            return true
        case command.startsWith("lesson do"):
            doLesson(command);
            return true
    }
    return false;
}

//done
async function joinTeam(c) {
    let teamCode = c.replace("team join ", "")
    if (teamCode) {
        const { data: { user } } = await supabase.auth.getUser();
        const apiurl = import.meta.env.VITE_API_URL
        const response = await fetch(apiurl + "/teams/user/join", {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
                user_id: user.id,
                team_code: teamCode,
            })
        });

        const data = await response.json()
        commandOutput(data.msg)
    }
}

async function leaveTeam(c) {
    let teamName = c.replace("team leave ", "")
    if (teamName) {
        const { data: { user } } = await supabase.auth.getUser();
        const apiurl = import.meta.env.VITE_API_URL
        const response = await fetch(apiurl + "/teams/user/leave", {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
                user_id: user.id,
                team_name: teamName,
            })
        });

        const data = await response.json()
        commandOutput(data.msg)
    }
}

async function getTeams() {
    let extra = await getUserExtra();

    if (extra.teams.length > 0) {
        let output = "\n"
        // optimize this
        for (let i = 0; i < extra.teams.length; i++) {
            // taken from https://stackoverflow.com/questions/1133770/how-to-convert-a-string-to-an-integer-in-javascript
            const { data, error } = await supabase.from("team").select("name").eq("id", parseInt(extra.teams[i]))

            if (error) {
                commandOutput("There is an issue with the teams you have joined - please contact support")
                return
            }

            output += i + 1 + '.\n name: "' + data[0].name + '"\n'
        }
        commandOutput(output)
        return
    } else {
        commandOutput("You are not a part of any team")
        return
    }
}

async function getLessons() {
    let extra = await getUserExtra();

    if (extra.teams.length > 0) {
        let output = "\n"
        let index = 1;

        for (let i = 0; i < extra.teams.length; i++) {
            // taken from https://stackoverflow.com/questions/1133770/how-to-convert-a-string-to-an-integer-in-javascript
            const { data, error } = await supabase.from("team").select("*").eq("id", parseInt(extra.teams[i]))
            const team = data

            if (error) {
                commandOutput("There is an issue with the teams you have joined - please contact support")
                return
            }

            let lessons = await getLesson(team[0].id)

            if (lessons.length > 0) {
                for (let i = 0; i < lessons.length; i++) {
                    output += index + ". \n" +
                        'lesson name: "' + lessons[i].name + '"\n' +
                        'from team: "' + team[0].name + '"\n' +
                        'starts: "' + lessons[i].start_time + '"\n' +
                        'ends: "' + lessons[i].end_time + '"\n'
                    index++
                }
            } else {
                output += 'No lesson for team "' + team[0].name + '" found \n'
            }
        }

        commandOutput(output)
        return
    } else {
        commandOutput("You need to join a team in order to get lessons")
        return
    }
}

async function doLesson(c){
    let lessonName = c.replace("lesson do ", "")

    if (lessonName) {
        const extra = await getUserExtra()
        if (extra) {
            const { data, error } = await supabase.from("lesson").select("*").eq("name", lessonName).eq("creator_id", extra.id)

            if (error) {
                commandOutput("There is a issue and we are not able to serve you now")
                return
            }

            if (data.length == 0) {
                commandOutput('No lesson with name "' + lessonName + '" found')
                return
            } else if (data.length > 1) {
                commandOutput('More then one lessons with name "' + lessonName + '" found - contact support')
                return
            } else {
                let todaysTime = new Date();
                let startTime = new Date(data[0].start_time);
                let endTime = new Date(data[0].end_time);

                if (startTime < todaysTime) {
                    if (endTime > todaysTime) {
                        console.log("go")
                    } else {
                        commandOutput("The lesson is already over")
                        return
                    }
                } else {
                    commandOutput("The lesson hasnt started yet")
                    return
                }
            }
        } else {
            commandOutput("Incomplete user profile - contact support")
            return
        }
    } else {
        commandOutput("No name provided - please provide a name")
    }
}

async function getLesson(team_id) {
    const { data, error } = await supabase.from("lesson").select("*").eq("team_id", team_id)

    if (error) {
        commandOutput("No team with id " + team_id + " found")
    }

    return data
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