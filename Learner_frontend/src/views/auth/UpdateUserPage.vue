<template>
    <div class="title-container">
        <pre class="ascii-container" id="ascii-art1">
 ____ ___            .___       __          
|    |   \______   __| _/____ _/  |_  ____  
|    |   /\____ \ / __ |\__  \\   __\/ __ \ 
|    |  / |  |_> > /_/ | / __ \|  | \  ___/ 
|______/  |   __/\____ |(____  /__|  \___  >
          |__|        \/     \/          \/ 
        </pre>
        <pre class="ascii-container" id="ascii-art2">
 ____  ____  ____  ____  _      ____  ____  ____ 
/  __\/  _ \/ ___\/ ___\/ \  /|/  _ \/  __\/  _ \
|  \/|| / \||    \|    \| |  ||| / \||  \/|| | \|
|  __/| |-||\___ |\___ || |/\||| \_/||    /| |_/|
\_/   \_/ \|\____/\____/\_/  \|\____/\_/\_\\____/
        </pre>
        <p class="title-warning-text">This is the page where you change your password</p>
        <hr class="title-hr">
    </div>
    <div class="main-container">
        <UpdateUserCommandLine />
    </div>
</template>

<script setup>
import UpdateUserCommandLine from '@/components/commandline/auth/UpdateUserCommandLine.vue'
import { onMounted } from 'vue'  

// generates the random color for the title
onMounted(() => {
    const random = Math.floor(Math.random() * 5);
    const colors1 = ["dark:text-blue-600", "dark:text-green-600", "dark:text-red-600", "dark:text-orange-600", "dark:text-violet-600",];
    const colors2 = ["dark:text-blue-600", "dark:text-green-600", "dark:text-red-600", "dark:text-orange-600", "dark:text-violet-600",];
    const ascii1 = document.getElementById("ascii-art1")
    const ascii2 = document.getElementById("ascii-art2")
    ascii1.classList.add(colors1[random])
    ascii2.classList.add(colors2[random])
})
</script>