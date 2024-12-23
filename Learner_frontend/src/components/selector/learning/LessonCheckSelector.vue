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
                <button class="selection-item-button" @click='router.push("/learning/admin")'>Exit</button>
            </div>
        </div>
        <div @click="currentIndex = 2">
            <div class="selections-item" :class="{ selected: currentIndex === 2 }">
                <button class="selection-item-button" :class="{ selected_button: currentIndex === 4, disabled_button: containerRunning == false }" @click='stopContainer'>Stop container</button>
            </div>
        </div>
        <div @click="currentIndex = 3">
            <div class="selections-item h-[60vh]" :class="{ selected: currentIndex === 3 }">
                <button class="selection-item-button h-16" v-if="!containerRunning" @click="startContainer">Start container</button>
                <iframe :src="url" width="100%" height="100%" frameborder="0" class="practice-cmd" v-if="containerRunning"></iframe>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { getContainer, getUserExtra } from '@/supabase/getFunctions.js'
import { supabase } from '@/supabase/init';

import { useRouter, useRoute } from 'vue-router'
const router = useRouter()
const route = useRoute()

let currentIndex = ref(0)
let containerRunning = ref(false)
let url = ref('')
const listLength = 4
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
    } else if (event.key === 'Enter' && currentIndex.value == 1) {
        router.push("/learning/admin")
    } else if (event.key === 'Enter' && currentIndex.value == 3) {
        startContainer()
    } else if (event.key === 'Enter' && currentIndex.value == 2) {
        stopContainer()
    }
}

async function startContainer() {
    const { data: { user } } = await supabase.auth.getUser();
    const apiurl = import.meta.env.VITE_API_URL
    const response = await fetch(apiurl + "/lessons/admin/start-container", {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
            user_id: user.id,
            container_id: container.value[0].id
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
    container.value = await getContainer({ id: containerId })
    let extra = await getUserExtra({ id: container.value[0].user_id })
    if (container.value[0].running) {
        containerRunning.value = true
    }
    userEmail.value = extra[0].email
    url.value = "http://127.0.0.1:" + container.value[0].port
}
</script>