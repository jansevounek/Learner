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
            <div class="selection-container-addon" @click="currentIndex = 1" :class="{ selected2: currentIndex === 1 }">
                <div class="mx-2">
                    <h1 class="selector-title">The task</h1>
                    <!--TODO change to task-->
                    <p>Task: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
                </div>
            </div>
            <div class="selection-container-addon" @click="currentIndex = 2" :class="{ selected2: currentIndex === 2 }">
                <div class="mx-2">
                    <h1 class="selector-title">Your workplace settigns</h1>
                    <p>Load allowed: {{ lesson.settings.load }}%</p>
                    <p>Network allowed: {{ lesson.settings.network }}</p>
                    <p>Sudo: {{ lesson.settings.sudo }}</p>
                </div>
            </div>
            <div class="selection-container-addon border-b-0 lg:border-b-2 h-16 flex justify-center items-center" @click="currentIndex = 3" :class="{ selected2: currentIndex === 3 }">
                <button class="selector-addon-button" :class="{ selected_button: currentIndex === 3 }" @click="router.push('/learning/user')">Exit</button>
            </div>
        </div>
        <div class="linux-container" @click="currentIndex = 4" :class="{ selected2: currentIndex === 4 }">
            <button class="linux-button" :class="{ selected_button: currentIndex === 4 }" @click="useContainer()" v-if="!containerExists">Create Container</button>
            <button class="linux-button" :class="{ selected_button: currentIndex === 4 }" @click="useContainer()" v-if="containerExists">Use Container</button>
            <!--<iframe :src="url" width="100%" height="100%" frameborder="0" class="practice-cmd"></iframe>-->
        </div>
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

const listLength = 5
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
            currentIndex.value = 4;
        }
    }  else if (event.key === 'ArrowRight') {
        if (currentIndex.value < 4) {
            lastControlIndex.value = currentIndex.value
        }
        horIndex.value = (horIndex.value + 1) % horLength;
        if (horIndex.value == 0) {
            currentIndex.value = lastControlIndex.value;
        } else if (horIndex.value == 1) {
            currentIndex.value = 4;
        }
    } else if (event.key === 'Enter' && currentIndex.value == 2) {
        router.push("/learning/user")
    } else if (event.key === 'Enter' && currentIndex.value == 4) {
        useContainer()
    }
}


async function useContainer() {
    const extra = await getUserExtra()
    const { data, error } = await supabase.from('container').select('*').eq('lesson_id', lessonId).eq('user_id', extra.id)

    console.log(data)
 
    if (error) {
        return
    }

    if (data.length == 1) {
        console.log("start container")
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
    }
}

async function setVariables() {
    const data = await getLesson({ id : lessonId })
    lesson.value = data[0]
    const extra = await getUserExtra()
    containerExists.value = await getContainer({ extra_id : extra[0].id, lesson_id : lessonId })
}
</script>