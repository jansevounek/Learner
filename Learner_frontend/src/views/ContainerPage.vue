<template>
    <div class="top-16 relative w-screen h-[80%]">
        <iframe :src="url" width="100%" height="100%" frameborder="0"></iframe>
        <br class="mb-16">
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute()

const url = ref('http://127.0.0.1:' + route.params.port)
</script>