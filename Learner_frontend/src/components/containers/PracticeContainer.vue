<template>
    <div class="practice-quit-container" :class="{'selected': currentIndex === 0}">
        <p class="underline font-mono" :class="{'selected': currentIndex === 0}">Quit Practice</p>
    </div>
    <div class="practice-cmd-container" :class="{'selected': currentIndex === 1}">
        <iframe :src="url" width="100%" height="100%" frameborder="0" class="practice-cmd"></iframe>
    </div>
    <br>
    <br>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useRoute } from 'vue-router'
const route = useRoute()
const router = useRouter()

let currentIndex = ref(1)
let fullsreen = ref(false)

onMounted(() => {
    window.addEventListener('keydown', handleKeyDown);
})

onUnmounted(() => {
    window.removeEventListener('keydown', handleKeyDown);
})

function handleKeyDown(event) {
    if (event.key === 'ArrowDown' || event.key === 's') {
        currentIndex.value = (currentIndex.value + 1) % 2;
        updateSelection(currentIndex.value);
    } else if (event.key === 'ArrowUp' || event.key === 'w') {
        currentIndex.value = (currentIndex.value - 1 + 2) % 2;
        updateSelection(currentIndex.value);
    } else if (event.key === 'Enter') {
        executeSelected()
    }
}

function executeSelected() {
    switch(currentIndex.value) {
        case 0:
            router.push('/')
            break

        case 1:
            router.push('/container/' + route.params.port)
            break
    }
}

function updateSelection(index) {
    currentIndex.value = index;
}

const url = ref('http://127.0.0.1:' + route.params.port)
</script>