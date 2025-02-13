<template>
    <div class="split-container" v-if="lesson">
        <div class="control-container">
            <div class="selection-container-addon" @click="currentIndex = 0" :class="{ selected2: currentIndex === 0 }">
                <div class="mx-2">
                    <h1 class="selector-title">Main info</h1>
                    <p>Name: "{{ lesson.name }}"</p>
                    <p>Ended at: "{{ lesson.end_time }}"</p>
                    <p class="text-red-600">Note: you cannot check solutions on a mobile device</p>
                </div>
            </div>
            <div class="selection-container-addon" @click="currentIndex = 1" :class="{ selected2: currentIndex === 1 }">
                <div class="mx-2">
                    <h1 class="selector-title">Task</h1>
                    <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Voluptatum, tenetur. Enim maiores, necessitatibus sint consequatur placeat ad commodi, fuga harum consectetur, atque dolorum veniam modi impedit laborum! Eos, iusto voluptate!</p>
                </div>
            </div>
            <div class="selection-container-addon border-b-0 lg:border-b-2 h-16 flex justify-center items-center" @click="currentIndex = 2" :class="{ selected2: currentIndex === 2 }">
                <button class="selector-addon-button" :class="{ selected_button: currentIndex === 2 }" @click="router.push('/learning/admin')">Exit</button>
            </div>
        </div>
        <div class="linux-container-items">
            <div class="container-list" v-if="containers.length > 0">
                <div class="container-list-item" v-for="(container, index) in containers" @click="currentIndex = 3 + index" :class="{ selected2: currentIndex === 3 + index }">
                    <p class="mx-auto" @click="selectContainer(index)">Container code-name: {{ container.name }}</p>
                    <p class="mx-auto" @click="selectContainer(index)">Container author: {{ container.email }}</p> 
                </div>
            </div>
            <div v-if="containers.length == 0"><p class="text-red-600 text-2xl">No completions created</p></div>
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
let containers = ref([])

let listLength = ref(3)
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
        currentIndex.value = (currentIndex.value + 1) % listLength.value;

        if (currentIndex.value >= 3) {
            lastControlIndex.value = 2
            horIndex.value = 1
        } else {
            horIndex.value = 0
            lastContainerIndex.value = listLength.value - 1
        }
    } else if (event.key === 'ArrowUp') {
        currentIndex.value = (currentIndex.value - 1 + listLength.value) % listLength.value;

        if (currentIndex.value >= 3) {
            lastControlIndex.value = 0
            horIndex.value = 1
        } else {
            horIndex.value = 0
            lastContainerIndex.value = 3
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
        exit()
    } else if (event.ctrlKey && event.key === 'c') {
        exit()
    }
}

function exit() {
    router.push('/learning/admin')
}

function selectContainer() {
    index = containers.value.length - (listLength.value - currentIndex.value)

    // taken from https://www.geeksforgeeks.org/how-to-detect-whether-the-website-is-being-opened-in-a-mobile-device-or-a-desktop-in-javascript/
    let details = navigator.userAgent; 

    let regexp = /android|iphone|kindle|ipad/i; 
    let isMobileDevice = regexp.test(details);

    if (!isMobileDevice) {
        router.push('/learning/solutions/container/' + containers.value[index].id)
    }
}

async function setVariables() {
    const data = await getLesson({ id : lessonId })
    lesson.value = data[0]
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