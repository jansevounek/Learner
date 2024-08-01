<template>
    <div class="fullscreen-container">
        <iframe :src="url" width="100%" height="100%" frameborder="0" class="practice-cmd"></iframe>
    </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
const route = useRoute()
const router = useRouter()

onMounted(() => {
    window.addEventListener('keydown', handleKeyDown);
})

onUnmounted(() => {
    window.removeEventListener('keydown', handleKeyDown);
})

function handleKeyDown(event) {
    if (event.ctrlKey && event.key === 'c') {
        router.go(-1)
    }
}

const url = ref('http://127.0.0.1:' + route.params.port)
</script>