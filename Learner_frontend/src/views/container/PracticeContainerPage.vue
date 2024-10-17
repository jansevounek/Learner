<template>
    <div class="title-container">
        <pre class="ascii-container text-lg lg:text-2xl" id="ascii-art">
_________              .___
\_   ___ \  _____    __| _/
/    \  \/ /     \  / __ | 
\     \___|  Y Y  \/ /_/ | 
 \______  /__|_|  /\____ | 
        \/      \/      \/
        </pre>
        <p class="title-warning-text">Here you are below is your practice container</p>
        <p class="title-ps-text">Time left: TODO</p>
        <hr class="title-hr">
    </div>
    <div class="main-container">
        <PracticeContainer />
    </div>
</template>

<script setup>
import PracticeContainer from '../../components/containers/PracticeContainer.vue'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute()

let displayContainer = ref(false)

const url = ref('http://127.0.0.1:' + route.params.port)

// generates the random color for the title
onMounted(() => {
    const random = Math.floor(Math.random() * 5);
    const colors = ["text-blue-600", "text-green-600", "text-red-600", "text-orange-600", "text-violet-600",];
    const ascii = document.getElementById("ascii-art")
    ascii.classList.add(colors[random])
})
</script>