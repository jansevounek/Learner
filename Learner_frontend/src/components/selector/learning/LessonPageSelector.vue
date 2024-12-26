<template>
    <div class="split-container" v-if="lesson">
        <div class="control-container">
            <div class="selection-container-addon" @click="currentIndex = 0" :class="{ selected2: currentIndex === 0 }">
                <div class="mx-2">
                    <h1 class="selector-title">Main info</h1>
                    <p>Name: "{{ lesson.name }}"</p>
                    <p>Started: "{{ lesson.start_time }}"</p>
                    <p>Ends in: "{{ lesson.end_time }}"</p>
                </div>
            </div>
            <div class="selection-container-addon" @click="currentIndex = 1" :class="{ selected2: currentIndex === 1 }" v-if="task">
                <div class="mx-2">
                    <h1 class="selector-title">The task</h1>
                    <!--TODO change to task-->
                    <p class="whitespace-nowrap" v-for="(line) in task">{{ line }}</p>
                </div>
            </div>
            <div class="selection-container-addon" @click="currentIndex = 2" :class="{ selected2: currentIndex === 2 }">
                <div class="mx-2">
                    <h1 class="selector-title">Your workplace settigns</h1>
                    <p>Network load allowed: {{ lesson.settings.network_load }}%</p>
                    <p>Cpu load allowed: {{ lesson.settings.cpu_load }}%</p>
                    <p>Network allowed: {{ lesson.settings.network }}</p>
                    <p>Sudo: {{ lesson.settings.sudo }}</p>
                </div>
            </div>
            <div class="selection-container-addon" @click="currentIndex = 3" :class="{ selected2: currentIndex === 3 }" v-if="containerExists">
                <div class="mx-2">
                    <h1 class="selector-title">Your container login</h1>
                    <div class="container-login-container">
                        <p>Login: {{ container[0].login }}</p>
                        <p class="ml-auto my-auto text-blue-700" @click="copyLogin()" id="login-copy">copy</p>
                    </div>
                    <div class="container-login-container">
                        <p>Password: {{ container[0].password }}</p>
                        <p class="ml-auto my-auto text-blue-700" @click="copyPassword()" id="password-copy">copy</p>
                    </div>
                </div>
            </div>
            <div class="selection-container-addon lg:border-b-2 h-16 flex justify-center items-center" @click="currentIndex = 4" :class="{ selected2: currentIndex === 4 }">
                <button class="selector-addon-button" :class="{ selected_button: currentIndex === 4 }" @click="router.push('/learning/user')">Exit</button>
            </div>
            <div class="selection-container-addon border-b-0 lg:border-b-2 h-16 flex justify-center items-center" @click="currentIndex = 5" :class="{ selected2: currentIndex === 5 }">
                <button class="selector-addon-button" :class="{ selected_button: currentIndex === 5, disabled_button: containerRunning == false }" @click="stopContainer()">Stop Container</button>
            </div>
        </div>
        <div class="linux-container" @click="currentIndex = 6" :class="{ selected2: currentIndex === 6 }">
            <button class="linux-button" :class="{ selected_button: currentIndex === 6 }" @click="useContainer()" v-if="!containerExists && !containerRunning">Create Container</button>
            <button class="linux-button" :class="{ selected_button: currentIndex === 6 }" @click="useContainer()" v-if="containerExists && !containerRunning">Use Container</button>
            <iframe :src="url" width="100%" height="100%" frameborder="0" class="practice-cmd" v-if="containerExists && containerRunning"></iframe>
        </div>
    </div>
    <div class="error-page-container" :class="{ flex: error_msg }">
        <p class="mt-2 ml-2 text-red-600">Error message: {{ error_msg }}</p>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { supabase } from '@/supabase/init.js'
import { getUserExtra, getLesson, getContainer } from '@/supabase/getFunctions.js'

// router import a setup
import { useRouter, useRoute } from 'vue-router'
const router = useRouter()
const route = useRoute()

let currentIndex = ref(0)
let horIndex = ref(0)
let lastControlIndex = ref(0);
let lesson = ref(false)
let containerExists = ref(false)
let containerRunning = ref(false)
let url = ref("")
let container = ref()
let error_msg = ref('')
let task = ref([])

const listLength = 6
const horLength = 2
const lessonId = route.params.id

// mounting handlers for controls
onMounted(() => {
    setVariables()
    window.addEventListener('keydown', handleKeyDown);
})

onUnmounted(() => {
    window.removeEventListener('keydown', handleKeyDown);
})

const handleRunningChange = (payload) => {
    if (payload.new.id == container.value[0].id) {
        if (!payload.new.running) {
            containerRunning.value = false
        } else if (payload.new.running) {
            containerRunning.value = true
        }
    }
}

supabase
  .channel('realtime')
  .on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'container' }, handleRunningChange)
  .subscribe()

function handleKeyDown(event) {
    if (event.key === 'ArrowDown') {
        currentIndex.value = (currentIndex.value + 1) % listLength;
    } else if (event.key === 'ArrowUp') {
        currentIndex.value = (currentIndex.value - 1 + listLength) % listLength;
    } else if (event.key === 'ArrowLeft') {
        if (currentIndex.value < 4) {
            lastControlIndex.value = currentIndex.value
        }
        horIndex.value = (horIndex.value - 1 + horLength) % horLength;
        if (horIndex.value == 0) {
            currentIndex.value = lastControlIndex.value;
        } else if (horIndex.value == 1) {
            currentIndex.value = 5;
        }
    }  else if (event.key === 'ArrowRight') {
        if (currentIndex.value < 4) {
            lastControlIndex.value = currentIndex.value
        }
        horIndex.value = (horIndex.value + 1) % horLength;
        if (horIndex.value == 0) {
            currentIndex.value = lastControlIndex.value;
        } else if (horIndex.value == 1) {
            currentIndex.value = 5;
        }
    } else if (event.key === 'Enter' && currentIndex.value == 4) {
        router.push("/learning/user")
    } else if (event.key === 'Enter' && currentIndex.value == 5) {
        stopContainer()
    } else if (event.key === 'Enter' && currentIndex.value == 6) {
        useContainer()
    }
}

function copyLogin() {
    let text1 = document.getElementById("login-copy")
    let text2 = document.getElementById("password-copy")
    navigator.clipboard.writeText(container.value[0].login);

    text1.textContent = "copied"
    text2.textContent = "copy"
}

function copyPassword() {
    let text1 = document.getElementById("password-copy")
    let text2 = document.getElementById("login-copy")
    navigator.clipboard.writeText(container.value[0].password);
    
    text1.textContent = "copied"
    text2.textContent = "copy"
}

function formatText() {
    let text = lesson.value.task
    let words = text.split(" ")
    const maxWords = 11
    const maxChars = 60
    const lines = []

    let currentLine = [];
    let currentLineLength = 0;

    for (const word of words) {
    
        if (word.length > maxChars) {
        
            if (currentLine.length > 0) {
                lines.push(currentLine.join(" "));
                currentLine = [];
                currentLineLength = 0;
            }


            for (let i = 0; i < word.length; i += maxChars) {
                lines.push(word.slice(i, i + maxChars));
            }
            continue;
        }

        if (
            currentLine.length + 1 > maxWords ||
            currentLineLength + word.length + (currentLine.length > 0 ? 1 : 0) > maxChars
        ) {
            lines.push(currentLine.join(" "));
            currentLine = [];
            currentLineLength = 0;
        }

        currentLine.push(word);
        currentLineLength += word.length + (currentLine.length > 1 ? 1 : 0);
    }

    if (currentLine.length > 0) {
        lines.push(currentLine.join(" "));
    }

    task.value = lines
}

async function useContainer() {
    const extra = await getUserExtra()
    const { data, error } = await supabase.from('container').select('*').eq('lesson_id', lessonId).eq('user_id', extra[0].id)
    
    if (error) {
        return
    }

    if (data.length == 1) {
        await startContainer(data)
    } else if (data.length > 1){
        console.log("error")
    } else {
        await createContainer()
    }
}

async function createContainer() {
    const { data: { user } } = await supabase.auth.getUser();
    const apiurl = import.meta.env.VITE_API_URL
    const response = await fetch(apiurl + "/lessons/user/create-container", {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
            user_id: user.id,
            lesson_id: lessonId,
        })
    });
    const data = await response.json()
    if (data.status) {
        containerExists.value = true
    } else {
        error_msg.value = data.msg
    }
}

async function startContainer(container) {
    const { data: { user } } = await supabase.auth.getUser();
    const apiurl = import.meta.env.VITE_API_URL
    const response = await fetch(apiurl + "/lessons/user/start-container", {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
            user_id: user.id,
            lesson_id: lessonId,
            container_id: container[0].id
        })
    });
    const data = await response.json()
    if (data.status) {
        containerRunning.value = true
    } else {
        error_msg.value = data.msg
    }
}

async function stopContainer() {
    if (containerRunning.value == true) {
        const apiurl = import.meta.env.VITE_API_URL
        const response = await fetch(apiurl + "/lessons/user/stop-container", {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: container.value[0].name,
            })
        });
        const data = await response.json()
        if (data.status) {
            containerRunning.value = false
        } else {
            error_msg.value = data.msg
        }
    }
}

async function setVariables() {
    const data = await getLesson({ id : lessonId })
    lesson.value = data[0]
    const extra = await getUserExtra()
    const c = await getContainer({ extra_id : extra[0].id, lesson_id : lessonId })
    if (c.length) {
        containerExists.value = true
        url.value = "http://127.0.0.1:" + String(c[0].port)
        if (c[0].running) {
            containerRunning.value = true
        }
    }
    container.value = c
    formatText()
}
</script>