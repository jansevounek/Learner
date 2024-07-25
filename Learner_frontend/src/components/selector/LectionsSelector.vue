<template>
    <div class="selections-container">
        <div v-for="(item, index) in items" :key="index" :ref="'item-n-' + index" @click="currentIndex = index">
            <div class="selections-item" :class="{ firstitem: index == 0, selected: currentIndex === index}">
                <h1 class="selections-item-content">Lection 1: Beginings</h1>
                <a class="selections-item-content text-blue-600" @click="displayDetails = !displayDetails">contents 
                    <span v-if="!displayDetails || currentIndex != index">▲</span>
                    <span v-if="displayDetails && currentIndex == index">▼</span>
                </a>
            </div>
            <div class="selections-item-details" v-if="displayDetails && currentIndex == index">
                <h1 class="item-details-title">Beginings</h1>
                <p class="text-center underline">Commands to learn:</p>
                <div class="item-details-commands">
                    <p class="selections-item-content text-blue-600">ls / ls -a</p>
                    <p class="selections-item-content text-blue-600">pwd</p>
                    <p class="selections-item-content text-blue-600">whoami</p>
                    <p class="selections-item-content text-blue-600">cd</p>
                </div>
                <p class="text-center underline">What you will learn:</p>
                <p class="mx-2 mb-2 text-center">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ducimus odit sint quam tenetur optio. Sit, a praesentium delectus blanditiis rerum perspiciatis nulla asperiores, consequuntur commodi nihil doloribus dolor inventore sunt.</p>
                <button class="start-lesson-button" @click="startLesson">Start lesson</button>
                <p class="start-lesson-text">To start lesson press enter again</p>
            </div>
        </div>
        <span class="mb-12"></span>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// router import a setup
import { useRouter } from 'vue-router'
const router = useRouter()

let displayDetails = ref(false)
const items = ref(['Item1', 'Item2', 'Item3', 'Item4'])
let currentIndex = ref(0)

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
        if (displayDetails.value) {
            //TODO lekce
            router.push('/')
        } else {
            displayDetails.value = true
        }
    } else if (event.key === 'Escape') {
        displayDetails.value = false
    } else if (event.ctrlKey && event.key === 'c') {
        router.push('/learning/homepage')
    }
}

function updateSelection(index) {
    currentIndex.value = index;
}

function startLesson() {
    console.log('start')
}
</script>