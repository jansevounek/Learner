<template>
    <div class="selections-container">
        <!--Name section-->
        <div @click="currentIndex = 0">
            <div class="selections-item" :class="{ selected: currentIndex === 0, firstitem: true }">
                <h1 class="selections-item-content">Name</h1>
                <a class="selections-item-content">name: 
                    <input type="text" class="cmd-input" v-focus="currentIndex === 0" v-model="nameInput">
                </a>
            </div>
        </div>
        <!--other section-->
        <div @click="currentIndex = 1">
            <div class="selections-item" :class="{ selected: currentIndex === 1}">
                <h1 class="selections-item-content">The task</h1>
                <a class="selections-item-content text-blue-600" @click="displayDetails = !displayDetails">expand 
                    <span v-if="!displayDetails || currentIndex != 1">▲</span>
                    <span v-if="displayDetails && currentIndex == 1">▼</span>
                </a>
            </div>
            <div class="selections-item-details" v-if="displayDetails && currentIndex == 1">
                <p class="text-center underline">Please input the desired task:</p>
                <textarea class="textarea-input" v-focus="displayDetails && currentIndex == 1" v-model="taskArea">
                </textarea>
            </div>
        </div>
        <div @click="currentIndex = 2">
            <div class="selections-item" :class="{ selected: currentIndex === 2}">
                <h1 class="selections-item-content">Container settings</h1>
                <a class="selections-item-content text-blue-600" @click="displayDetails = !displayDetails">expand 
                    <span v-if="!displayDetails || currentIndex != 2">▲</span>
                    <span v-if="displayDetails && currentIndex == 2">▼</span>
                </a>
            </div>
            <div class="selections-item-details h-60" v-if="displayDetails && currentIndex == 2">
                <div class="item-details-checkbox-container" :class="{ selected: subIndex === 0}">
                    <div class="item-details-checkbox" :class="{ checboxSelected: networkSelected }" @click="networkSelected = !networkSelected"></div>
                    <label class="mr-1">Network required</label>
                </div>
                <div class="item-details-checkbox-container" :class="{ selected: subIndex === 1}">
                    <div class="item-details-checkbox" :class="{ checboxSelected: sudoSelected }" @click="sudoSelected = !sudoSelected"></div>
                    <label class="mr-1">Sudo required</label>
                </div>
                <div class="item-detail-input-container" :class="{ selected: subIndex === 2}">
                    <p class="mx-2">What load is allowed</p>
                    <input type="text" class="item-detail-input" placeholder="0-100" v-model="loadInput" v-focus="displayDetails && currentIndex == 2 && subIndex == 2">
                </div>
            </div>
        </div>
        <span class="mb-12"></span>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { supabase } from '@/supabase/init.js'

// router import a setup
import { useRouter } from 'vue-router'
const router = useRouter()

let displayDetails = ref(false)
let currentIndex = ref(0)
let subIndex = ref(0)

let taskArea = ref('')
let nameInput = ref('')
let networkSelected = ref(false)
let sudoSelected = ref(false)
let loadInput = ref('')

const listLength = 3
const subListLength = 3

// mounting handlers for controls
onMounted(() => {
    window.addEventListener('keydown', handleKeyDown);
})

onUnmounted(() => {
    window.removeEventListener('keydown', handleKeyDown);
})

const vFocus = {
    mounted(el, binding) {
        if (binding.value) {
            el.focus();
        }
    },
    updated(el, binding) {
        if (binding.value) {
            el.focus();
        }
    }
}

function handleKeyDown(event) {
    if (event.key === 'ArrowDown' && event.ctrlKey) {
        if (displayDetails.value && currentIndex.value == 2) {
            subIndex.value = (subIndex.value + 1) % subListLength;
        }
    } else if (event.key === 'ArrowUp' && event.ctrlKey) {
        if (displayDetails.value && currentIndex.value == 2) {
            subIndex.value = (subIndex.value - 1 + subListLength) % subListLength;
        }
    } else if (event.key === 'ArrowDown') {
        displayDetails.value = false
        currentIndex.value = (currentIndex.value + 1) % listLength;
        updateSelection(currentIndex.value);
    } else if (event.key === 'ArrowUp') {
        displayDetails.value = false
        currentIndex.value = (currentIndex.value - 1 + listLength) % listLength;
        updateSelection(currentIndex.value);
    } else if (event.key === 'Enter' && event.ctrlKey) {
        selectContainerOptions()
    } else if (event.key === 'Enter') {
        displayDetails.value = !displayDetails.value
    } else if (event.key === 'Escape') {
        displayDetails.value = false
    } else if (event.ctrlKey && event.key === 'c') {
        router.push('/learning/admin')
    }
}

function updateSelection(index) {
    currentIndex.value = index;
}

function selectContainerOptions() {
    if (subIndex.value === 0) {
        networkSelected.value = !networkSelected.value
    } else if (subIndex.value === 1) {
        sudoSelected.value = !sudoSelected.value
    }
}
</script>