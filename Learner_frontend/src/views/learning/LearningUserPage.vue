<template>
    <div class="title-container">
    <pre class="ascii-container text-[6px] lg:text-sm" id="ascii-art">                                                                                          
.----------------.  .----------------.  .----------------.  .----------------.  .-----------------.
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |   _____      | || |  _________   | || |      __      | || |  _______     | || | ____  _____  | |
| |  |_   _|     | || | |_   ___  |  | || |     /  \     | || | |_   __ \    | || ||_   \|_   _| | |
| |    | |       | || |   | |_  \_|  | || |    / /\ \    | || |   | |__) |   | || |  |   \ | |   | |
| |    | |   _   | || |   |  _|  _   | || |   / ____ \   | || |   |  __ /    | || |  | |\ \| |   | |
| |   _| |__/ |  | || |  _| |___/ |  | || | _/ /    \ \_ | || |  _| |  \ \_  | || | _| |_\   |_  | |
| |  |________|  | || | |_________|  | || ||____|  |____|| || | |____| |___| | || ||_____|\____| | |
| |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 
    </pre>
    <p class="title-warning-text">On this site you can take your lessons and test</p>
    <p class="title-ps-text">PS: and join teams</p>
    <hr class="title-hr">
  </div>
  <div class="main-container">
    <UserCommandLine />
  </div>
</template>

<script setup>
import UserCommandLine from '@/components/commandline/learning/UserCommandLine.vue'
import { onMounted } from 'vue'

// generates the random color for the title
onMounted(() => {
    const random = Math.floor(Math.random() * 5);
    const colors = ["dark:text-blue-600", "dark:text-green-600", "dark:text-red-600", "dark:text-orange-600", "dark:text-violet-600",];
    const ascii = document.getElementById("ascii-art")
    ascii.classList.add(colors[random])
})
</script>