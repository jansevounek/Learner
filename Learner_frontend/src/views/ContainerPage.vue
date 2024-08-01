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
        <p class="title-warning-text">Dont worry you are on the right page - dont run away and try typing "help"</p>
        <p class="title-ps-text">PS: this site is meant to look like this and you will soon see why</p>
        <hr class="title-hr">
    </div>
    <div class="main-container">
        <PracticeCommandLine />
    </div>
        <!--<iframe :src="url" width="100%" height="100%" frameborder="0" ></iframe>-->
</template>

<script setup>
import PracticeCommandLine from '../components/commandline/PracticeCommandLine.vue'
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