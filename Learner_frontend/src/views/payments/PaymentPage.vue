<template>
    <div class="title-container">
        <pre class="ascii-container text-[10px]" id="ascii-art1">                                     
______  ______ ______   _____  ______   _____  
\     \|\     \\     \  \    \|\     \ |     | 
 |     |\|     |\    |  |    |\ \     \|     | 
 |     |/____ /  |   |  |    | \ \           | 
 |     |\     \  |    \_/   /|  \ \____      | 
 |     | |     | |\         \|   \|___/     /| 
 |     | |     | | \         \__     /     / | 
/_____/|/_____/|  \ \_____/\    \   /_____/  / 
|    |||     | |   \ |    |/___/|   |     | /  
|____|/|_____|/     \|____|   | |   |_____|/   
                          |___|/               
        </pre>
        <pre class="ascii-container text-[10px]" id="ascii-art2">
 ____  ____     ___  ___ ___  ____  __ __  ___ ___ 
|    \|    \   /  _]|   |   ||    ||  |  ||   |   |
|  o  )  D  ) /  [_ | _   _ | |  | |  |  || _   _ |
|   _/|    / |    _]|  \_/  | |  | |  |  ||  \_/  |
|  |  |    \ |   [_ |   |   | |  | |  :  ||   |   |
|  |  |  .  \|     ||   |   | |  | |     ||   |   |
|__|  |__|\_||_____||___|___||____| \__,_||___|___|
                                                   
        </pre>
        <p class="title-warning-text">Here you can pay for the premium version of our application</p>
        <p class="title-ps-text">It includes ...</p>
        <hr class="title-hr">
    </div>
    <div class="main-container">
        <PaymentCommandLine/>
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import PaymentCommandLine from '@/components/commandline/payments/PaymentCommandLine.vue'

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