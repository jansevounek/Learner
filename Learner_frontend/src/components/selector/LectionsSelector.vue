<template>
    <div class="selections-container">
        <div v-for="(item, index) in items" :key="index" :ref="'item-n-' + index" @click="currentIndex = index">
            <div class="selections-item" :class="{ firstitem: index == 0, selected: currentIndex === index}">
                <h1 class="selections-item-content">Lection {{ index + 1 }}: {{ item.name }}</h1>
                <a class="selections-item-content text-blue-600" @click="displayDetails = !displayDetails">contents 
                    <span v-if="!displayDetails || currentIndex != index">▲</span>
                    <span v-if="displayDetails && currentIndex == index">▼</span>
                </a>
            </div>
            <div class="selections-item-details" v-if="displayDetails && currentIndex == index">
                <h1 class="item-details-title">{{ item.name }}</h1>
                <p class="text-center underline">Commands to learn:</p>
                <div class="item-details-commands">
                    <p class="selections-item-content text-blue-600" v-for="(command) in item.commands">{{ command }}</p>
                </div>
                <p class="text-center underline">What you will learn:</p>
                <p class="mx-2 lg:mx-80 mb-2 text-center">{{ item.description }}</p>
                <button class="start-lesson-button" @click="startLesson(item.id)">Click here to start lesson</button>
            </div>
        </div>
        <span class="mb-12"></span>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { supabase } from '../../supabase/init.js'

// router import a setup
import { useRouter } from 'vue-router'
const router = useRouter()

let displayDetails = ref(false)
const items = ref([])
let currentIndex = ref(0)

getLections()
// mounting handlers for controls
onMounted(() => {
    window.addEventListener('keydown', handleKeyDown);
})

onUnmounted(() => {
    window.removeEventListener('keydown', handleKeyDown);
})

function handleKeyDown(event) {
    if (event.key === 'ArrowDown' || event.key === 's') {
        displayDetails.value = false
        currentIndex.value = (currentIndex.value + 1) % items.value.length;
        updateSelection(currentIndex.value);
    } else if (event.key === 'ArrowUp' || event.key === 'w') {
        displayDetails.value = false
        currentIndex.value = (currentIndex.value - 1 + items.value.length) % items.value.length;
        updateSelection(currentIndex.value);
    } else if (event.key === 'Enter') {
        displayDetails.value = !displayDetails.value
    } else if (event.key === 'Escape') {
        displayDetails.value = false
    } else if (event.ctrlKey && event.key === 'c') {
        router.push('/learning/homepage')
    }
}

async function getLections() {
    const { data, error } = await supabase
        .from("lections")
        .select("*")

    if (error) {
        console.log("problem getting lections")
    }

    items.value = data
}

function updateSelection(index) {
    currentIndex.value = index;
}

function startLesson(id) {
    router.push('/learning/lection/' + id)
}
</script>