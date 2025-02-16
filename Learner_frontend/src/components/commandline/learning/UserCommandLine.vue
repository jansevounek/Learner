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
import { getUser, getTeam, getLesson, getUserExtra } from '@/supabase/getFunctions.js'

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
    if (cmdinput.value !== ''){
        executedList.value.push(cmdinput.value)
        executedIndex.value = executedList.value.length
    }
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
            printTeams();
            return true
        // done
        case command == "lesson ps":
            printLessons();
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
        const user = await getUser();
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
        const user = await getUser();
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

async function printTeams() {
    const team = await getTeam()

    if (team.length > 0) {
        let output = "\n"

        for (let i = 0; i < team.length; i++) {
            output += i + 1 + '.\n name: "' + team[i].name + '"\n'
        }

        commandOutput(output)
        return
    } else {
        commandOutput("You are not a part of any team")
        return
    }
}

async function printLessons() {
    const team = await getTeam()

    if (team.length > 0) {
        let output = "\n"
        let index = 1;

        for (let i = 0; i < team.length; i++) {
            let lessons = await getLesson({ team_id: team[i].id })

            if (lessons.length > 0) {
                for (let k = 0; k < lessons.length; k++) {
                    output += index + ". \n" +
                        'lesson name: "' + lessons[k].name + '"\n' +
                        'from team: "' + team[i].name + '"\n' +
                        'starts: "' + lessons[k].start_tkme + '"\n' +
                        'ends: "' + lessons[k].end_time + '"\n'
                    index++
                }
            } else {
                output += 'No lesson for team "' + team[i].name + '" found \n'
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
    const extra = await getUserExtra()

    // taken from https://www.geeksforgeeks.org/how-to-detect-whether-the-website-is-being-opened-in-a-mobile-device-or-a-desktop-in-javascript/
    let details = navigator.userAgent; 

    let regexp = /android|iphone|kindle|ipad/i; 
    let isMobileDevice = regexp.test(details);

    if (lessonName) {
        if (!isMobileDevice) {
            const lesson = await getLesson({ name: lessonName })
            const teams = await getTeam()

            if (lesson.length == 0) {
                commandOutput('No lesson with name "' + lessonName + '" found')
                return
            } else if (lesson.length > 1) {
                commandOutput('More then one lessons with name "' + lessonName + '" found - contact support')
                    return
            } else {
                if (lesson[0].creator_id !== extra[0].id) {
                    for (let i = 0; i < teams.length; i++) {
                        if (lesson[0].team_id == teams[i].id) {
                            let todaysTime = new Date();
                            let startTime = new Date(lesson[0].start_time);
                            let endTime = new Date(lesson[0].end_time);
                            if (startTime < todaysTime) {
                                if (endTime > todaysTime) {
                                    router.push("/learning/lesson/" + lesson[0].id)
                                } else {
                                    commandOutput("The lesson is already over")
                                    return
                                }
                            } else {
                                commandOutput("The lesson hasnt started yet")
                                return
                            }
                        } else {
                            commandOutput("The lesson does not exist")
                            return
                        }

                    }

                    commandOutput('No lesson with name "' + lessonName + '" found')
                    return
                } else {
                    commandOutput('You cannot do a lesson you have created')
                    return
                }
            }
        } else {
            commandOutput("You cannot do a lesson on a mobile device")
        }
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

function getHelp() {
    commandOutput('\nTo navigate and use THIS PART of the application you can use these commands: \n' +
            '\n' +
            ' Essential commands: \n' +
            ' "help" - this command displayed this info about how to use the app \n' +
            ' "go " + (number / The name written below the number "Home", etc.) - this command lets you navigate throw our app (by chosing the number written above the place you want to go in the navigation bar) \n' +
            ' "clear" - using this command simply clears the lines that you writing your commands created \n \n' +
            ' Team related commands: \n' +
            ' "team join <code>" - here the "<code>" is replaced with a code that you receive from the team owner and is used to enter a team in which you receive the task to do. (code format is "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx") \n' +
            ' "team leave <name>" - The "<name>" tag is in this instance replaced with the name of the team you wnat to leave - yes this command is used to leave teams that you joined \n' +
            ' "team ps" - This command simply tells you which teams you are already part of \n \n' +
            ' Lessons related commands: \n' +
            ' "lesson ps" - As it is with teams this command just simply displays all the different lessons that you can do \n' +
            ' "lesson do <name>" - In this instance the <name> tag is replaced with the name of the lesson you want to do \n \n' +
            ' Extra commands: \n' +
            ' "Github" - This command takes you to the github page of this web application \n' +
            ' "Socials" - This command takes you to the social pages of this application \n' +
            ' "License" - This command displays the MIT license under which the application is published \n'
            )
}

function clearLines() {
    executedCommands.value = ''
    cmdinput.value = ''
}

function changeCommand(){
    cmdinput.value = executedList.value[executedIndex.value]
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