<template>
    <div class="title-container">
        <pre class="ascii-container" id="ascii-art1">
   __                _   
  /__\ ___  ___  ___| |_ 
 / \/// _ \/ __|/ _ \ __|
/ _  \  __/\__ \  __/ |_ 
\/ \_/\___||___/\___|\__|
        </pre>
        <pre class="ascii-container" id="ascii-art2">
 ____ ___  ___  ___  _  _ ____ ____ ___  
| . \|  \ | _\ | _\ ||| \|   || . \|  \ 
| __/| . \[__ \[__ \||\ /| . ||  <_| . \
|/   |/\_/|___/|___/|/\/ |___/|/\_/|___/
        </pre>
        <p class="title-warning-text">This is the page where you reset your password - simply just type in your email.</p>
        <p class="title-ps-text">You will be sent your email shortly after.</p>
        <hr class="title-hr">
    </div>
    <ResetPasswordCommandLine />
</template>

<script setup>
import ResetPasswordCommandLine from '@/components/commandline/auth/ResetPasswordCommandLine.vue'
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