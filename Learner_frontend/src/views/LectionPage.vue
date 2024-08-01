<template>
    <div class="title-container">
        <pre class="ascii-container" id="ascii-art">
{{ titleText }}
        </pre>
        <p class="title-warning-text">Lets learn:</p>
        <p class="title-ps-text text-green-600">{{ description }}</p>
        <hr class="title-hr">
    </div>
    <div class="main-container">
        <LectionCommandLine />
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import LectionCommandLine from '../components/commandline/LectionCommandLine.vue'
import figlet from 'figlet'
import Rectangles from "figlet/importable-fonts/Rectangles.js";
import { supabase } from '../supabase/init.js'
import { useRoute } from 'vue-router'

const titleText = ref('')
const route = useRoute()
const description = ref('')

// generates the random color for the title
onMounted(() => {
    getColor()
    getText()
})

async function getText() {
    const { data, error } = await supabase
        .from("lections")
        .select("*")
        .eq("id", route.params.id)

        description.value = data[0].description
    
    figlet.parseFont("Rectangles", Rectangles);

    figlet.text(
      data[0].name,
      {
        font: "Rectangles",
      },
      function (err, data) {
        titleText.value = data;
      }
    );
}

function getColor() {
    const random = Math.floor(Math.random() * 5);
    const colors = ["text-blue-600", "text-green-600", "text-red-600", "text-orange-600", "text-violet-600",];
    const ascii = document.getElementById("ascii-art")
    ascii.classList.add(colors[random])
}
</script>