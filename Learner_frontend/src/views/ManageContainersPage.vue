<template>
    <div class="title-container">
        <pre class="ascii-container text-[10px] lg:text-sm" id="ascii-art1">
   _____                                       
  /     \ _____    ____ _____     ____   ____  
 /  \ /  \\__  \  /    \\__  \   / ___\_/ __ \ 
/    Y    \/ __ \|   |  \/ __ \_/ /_/  >  ___/ 
\____|__  (____  /___|  (____  /\___  / \___  >
        \/     \/     \/     \//_____/      \/ 
        </pre>
        <pre class="ascii-container text-[10px] lg:text-sm" id="ascii-art2">
 ____  ____  _      _____  ____  _  _      _____ ____  ____ 
/   _\/  _ \/ \  /|/__ __\/  _ \/ \/ \  /|/  __//  __\/ ___\
|  /  | / \|| |\ ||  / \  | / \|| || |\ |||  \  |  \/||    \
|  \__| \_/|| | \||  | |  | |-||| || | \|||  /_ |    /\___ |
\____/\____/\_/  \|  \_/  \_/ \|\_/\_/  \|\____\\_/\_\\____/
                                                            
        </pre>
        <p class="title-warning-text">This is the page from where you use your container</p>
        <p class="title-ps-text">PS: try typing "help"</p>
        <hr class="title-hr">
    </div>
    <div class="main-container">
        <ManageContainersCommandLine />
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import ManageContainersCommandLine from '@/components/commandline/ManageContainersCommandLine.vue'

// generates the random color for the title
onMounted(() => {
    const random = Math.floor(Math.random() * 5);
    const colors1 = ["text-blue-600", "text-green-600", "text-red-600", "text-orange-600", "text-violet-600",];
    const colors2 = ["text-violet-600", "text-orange-600", "text-blue-600", "text-green-600", "text-red-600",];
    const ascii1 = document.getElementById("ascii-art1")
    const ascii2 = document.getElementById("ascii-art2")
    ascii1.classList.add(colors1[random])
    ascii2.classList.add(colors2[random])
})
</script>