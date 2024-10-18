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
        case "Home":
        case "go 1":
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
        //done
        case command.startsWith("team create"):
            createTeam(command);
            return true
        case command === "team ps":
            getTeams();
            return true
        case command.startsWith("team delete"):
            deleteTeam(command);
            return true
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
        let extra = await getUserExtra()
        if (extra) {
            const { data, error } = await supabase
                .from('limitations')
                .select('team_limit, teams')
                .eq('extra_id', extra.id);
            if (error) {
                commandOutput("User profile incomplete please contact support")
                return;
            }
            if (data) {
                if (data[0].team_limit > data[0].teams) {
                    const { error } = await supabase
                        .from("team")
                        .insert({ name: name, creator_id: extra.id })

                    if (error) {
                        console.log(error)
                        commandOutput("Failed to create your team - contact support")
                        return;
                    } else {
                        let count = data[0].teams + 1
                        const { error } = await supabase
                            .from("limitations")
                            .update({ teams: count })
                            .eq('extra_id', extra.id)

                        if (error) {
                            console.log(error)
                            commandOutput("idk - Contact support")
                            return;
                        }
                    }
                } else {
                    commandOutput("You have reached your maximum of created teams")
                    return;
                }
            }
        } else {
            commandOutput("User profile incomplete please contact support")
            return;
        }
        commandOutput('Team "' + name + '" successfully created')
        return;
    } else {
        commandOutput("Please provide a name for the team")
        return;
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
            commandOutput("Failed to get your teams - contact support")
            return
        }

        printTeams(data)
    } else {
        commandOutput("Failed to get your teams - contact support")
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
        let extra = await getUserExtra()

        if (extra) {
            const { data, error } = await supabase
                .from("team")
                .delete()
                .eq("name", name)
                .eq("creator_id", extra.id)
                .select()

            if (error) {
                commandOutput("An error occured while trying to delete a team - contact support")
                return
            }

            if (data.length) {
                const limit = await getLimitations()
                if (limit) {
                    let count = limit.teams - data.length
                    const { error } = await supabase
                        .from("limitations")
                        .update({ teams: count })
                        .eq('extra_id', extra.id)

                    if (error) {
                        console.log(error)
                        commandOutput("You used delete - critical hit")
                        return
                    }

                    let output = "user@linuxlearning:~$ " + cmdinput.value + "\n Deleted team(s):";

                    for (let i = 0; i < data.length; i++) {
                        output += ' "' + data[i].name + '",';
                    }
                    // taken from https://stackoverflow.com/questions/952924/how-do-i-chop-slice-trim-off-last-character-in-string-using-javascript
                    output = output.slice(0, -1)

                    commandOutput(output)
                }
            } else {
                commandOutput("No teams deleted")
                return
            }
        } else {
            commandOutput("User profile incomplete please contact support")
            return;
        }
    } else {
        commandOutput("Please provide a name of a team you want to delete")
    }
}

function createLesson() {

}

function cancelLesson() {

}

function getLessons() {

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
</script>