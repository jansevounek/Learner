<template>
    <div class="split-container" v-if="lesson">
        <div class="control-container">
            <div class="selection-container-addon" @click="currentIndex = 0" :class="{ selected2: currentIndex === 0 }">
                <div class="mx-2">
                    <h1 class="selector-title">Main info</h1>
                    <p>Name: "{{ lesson.name }}"</p>
                    <p>Ended at: "{{ lesson.end_time }}"</p>
                </div>
            </div>
            <div class="selection-container-addon" @click="currentIndex = 1" :class="{ selected2: currentIndex === 1 }">
                <div class="mx-2">
                    <h1 class="selector-title">Settigns</h1>
                    <p>Network load allowed: {{ lesson.settings.network_load }}%</p>
                    <p>Cpu load allowed: {{ lesson.settings.cpu_load }}%</p>
                    <p>Network allowed: {{ lesson.settings.network }}</p>
                    <p>Sudo: {{ lesson.settings.sudo }}</p>
                </div>
            </div>
            <div class="selection-container-addon border-b-0 lg:border-b-2 h-16 flex justify-center items-center" @click="currentIndex = 2" :class="{ selected2: currentIndex === 2 }">
                <button class="selector-addon-button" :class="{ selected_button: currentIndex === 2,}" @click="changeContainer()" v-if="!containerRunning && containerPickedId">Change Container</button>
                <button class="selector-addon-button" :class="{ selected_button: currentIndex === 2 }" @click="router.push('/learning/admin')" v-if="!containerRunning && !containerPickedId">Exit</button>
                <button class="selector-addon-button" :class="{ selected_button: currentIndex === 2 }" @click="stopContainer()" v-if="containerRunning && containerPickedId">Stop container</button>
            </div>
        </div>
        <div class="linux-container" v-if="!containerPickedId">
            <div class="container-list" v-if="containers">
                <div class="container-list-item" v-for="(container, index) in containers" @click="currentIndex = 3 + index" :class="{ selected2: currentIndex === 3 + index }">
                    <p class="mx-auto">Container code-name: {{ container.name }}</p>
                    <p class="mx-auto">Container author: {{ container.email }}</p>
                    <button class="cmd-input-mobile-btn mb-0" @click="selectContainer()">Check container</button>
                </div>
            </div>
        </div>
        <div class="linux-container" v-if="containerPickedId" @click="currentIndex = 3" :class="{ selected2: currentIndex === 3 }">
            <div>
                <button class="linux-button" :class="{ selected_button: currentIndex === 3 }" @click="useContainer()" v-if="!containerRunning">Check Container</button>
                <iframe :src="url" width="100%" height="100%" frameborder="0" class="practice-cmd" v-if="containerRunning"></iframe>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { getLesson, getContainer, getUserExtra } from '@/supabase/getFunctions.js'

import { useRouter, useRoute } from 'vue-router'
const router = useRouter()
const route = useRoute()

let currentIndex = ref(0)
let horIndex = ref(0)
let lastControlIndex = ref(0)
let lastContainerIndex = ref(0)

let lesson = ref()
let containers = ref([[]])

let containerRunning = ref(false)
let url = ref('')
let containerPickedId = ref(false)
let pickedId = ref(-1)

let listLength = ref(4)
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
    console.log(listLength.value)
    if (event.key === 'ArrowDown') {
        currentIndex.value = (currentIndex.value + 1) % listLength.value;
        if (currentIndex.value == 4) {
            lastControlIndex.value = 3
        }
    } else if (event.key === 'ArrowUp') {
        currentIndex.value = (currentIndex.value - 1 + listLength.value) % listLength.value;
        if (currentIndex.value == 4) {
            lastControlIndex.value = 3
        }
    } else if (event.key === 'ArrowLeft') {
        if (currentIndex.value < 3) {
            lastControlIndex.value = currentIndex.value
        } else if (currentIndex.value >= 3) {
            lastContainerIndex.value = currentIndex.value
        }
        horIndex.value = (horIndex.value - 1 + horLength) % horLength;
        if (horIndex.value == 0) {
            currentIndex.value = lastControlIndex.value;
        } else if (horIndex.value == 1) {
            currentIndex.value = lastContainerIndex.value
        }
    } else if (event.key === 'ArrowRight') {
        if (currentIndex.value < 3) {
            lastControlIndex.value = currentIndex.value
        } else if (currentIndex.value >= 3) {
            lastContainerIndex.value = currentIndex.value
        }
        horIndex.value = (horIndex.value + 1) % horLength;
        if (horIndex.value == 0) {
            currentIndex.value = lastControlIndex.value;
        } else if (horIndex.value == 1) {
            currentIndex.value = lastContainerIndex.value
        }
    } else if (event.key === "Enter" && currentIndex.value >= 3) {
        selectContainer()
    } else if (event.key === "Enter" && currentIndex.value == 2) {
        useControlButton()
    }
}

function useControlButton() {
    console.log(currentIndex.value)
    if (!containerRunning.value && containerPickedId.value) {
        console.log("now")
        changeContainer()
    } else if (!containerRunning.value && !containerPickedId.value) {
        router.push('/learning/admin')
    } else if (containerRunning.value && containerPickedId.value) {
        stopContainer()
    }
}

function stopContainer() {

}

function selectContainer() {
    containerPickedId.value = true
    pickedId.value = currentIndex.value - containers.value.length
    listLength.value = 4
}

function changeContainer() {
    containerPickedId.value = false
    pickedId.value = -1
    listLength.value = 3 + containers.value.length
}

async function setVariables() {
    const data = await getLesson({ id : lessonId })
    lesson.value = data[0]
    url.value = lesson.value.port
    if (lesson) {
        containers.value = await getContainer({ lesson_id: lessonId })
        listLength.value = 3 + containers.value.length
        for (let i = 0; i < containers.value.length; i ++) {
            let extra = await getUserExtra({ id: containers.value[i].user_id })
            
            containers.value[i].email = extra[0].email
        }
    }
}
</script>