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
                <button class="selection-item-button" @click='router.back()'>Exit</button>
            </div>
        </div>
        <div @click="currentIndex = 2">
            <div class="selections-item" :class="{ selected: currentIndex === 2 }">
                <button class="selection-item-button" :class="{ selected_button: currentIndex === 4, disabled_button: siteState == 'start' }" @click='stopContainer'>Stop container</button>
            </div>
        </div>
        <div @click="currentIndex = 3">
            <div class="selections-item h-[60vh]" :class="{ selected: currentIndex === 3 }">
                <button class="selection-item-button h-16" v-if="siteState == 'start'" @click="startContainer">Start container</button>
                <p class="font-mono text-green-600 mx-auto" v-if="siteState == 'starting'">Starting the container ...</p>
                <p class="font-mono text-green-600 mx-auto" v-if="siteState == 'stoping'">Stoping the container ...</p>
                <iframe :src="url" width="100%" height="100%" frameborder="0" class="practice-cmd" v-if="siteState == 'running'"></iframe>
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
let siteState = ref("start")
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
        // Taken from https://www.geeksforgeeks.org/how-to-go-back-route-back-on-vue-router/
        router.back()
    } else if (event.key === 'Enter' && currentIndex.value == 3) {
        startContainer()
    } else if (event.key === 'Enter' && currentIndex.value == 2) {
        stopContainer()
    }
}

async function startContainer() {
    if (siteState.value == "start") {
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
            siteState.value = "starting"
            console.log(siteState.value)

            // Timeout from https://stackoverflow.com/questions/951021/what-is-the-javascript-version-of-sleep
            await new Promise(r => setTimeout(r, 9000));

            siteState.value = "running"
            console.log(siteState.value)
        } else {
            error_msg.value = data.msg
        }
    }
}

async function stopContainer() {
    if (siteState.value == "running") {
        siteState.value = "stoping"
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
            siteState.value = "start"
        } else {
            error_msg.value = data.msg
        }
    }
}

async function setVariables() {
    container.value = await getContainer({ id: containerId })
    let extra = await getUserExtra({ id: container.value[0].user_id })
    if (container.value[0].running) {
        siteState.value = "running"
    }
    userEmail.value = extra[0].email
    url.value = "http://127.0.0.1:" + container.value[0].port
}
</script>