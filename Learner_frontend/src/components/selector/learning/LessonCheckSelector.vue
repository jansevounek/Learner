<template>
    <div class="selections-container" v-if="container">
        <div @click="currentIndex = 0">
            <div class="selections-item flex-col lg:flex-row" :class="{ selected: currentIndex === 0, firstitem: true }">
                <h1 class="selections-item-content mt-1 lg:mt-0">Container name: {{ container[0].name }}</h1>
                <h1 class="selections-item-content">Creator: {{ userEmail }}</h1>
            </div>
        </div>
        <div @click="currentIndex = 1">
            <div class="selections-item" :class="{ selected: currentIndex === 1 }">
                <b class="selection-item-button" @click="createLesson">Exit</b>
            </div>
        </div>
        <div @click="currentIndex = 2">
            <div class="selections-item h-[60vh]" :class="{ selected: currentIndex === 2 }">
                
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { getContainer, getUserExtra } from '@/supabase/getFunctions.js'

import { useRouter, useRoute } from 'vue-router'
const router = useRouter()
const route = useRoute()

let currentIndex = ref(0)
const listLength = 3
const container = ref()
const userEmail = ref()
const containerId = route.params.id

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
    }
}

async function setVariables() {
    container.value = await getContainer({ id: containerId })
    let extra = await getUserExtra({ id: container.value[0].user_id })
    userEmail.value = extra[0].email
}
</script>