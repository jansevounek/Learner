<template>
    <div class="title-container">
        <pre class="ascii-container text-[6px] lg:text-sm" id="ascii-art">                                                                                          
 ____             ______          ____        _____  _____   ______        ______        _____   
|    |        ___|\     \    ____|\   \   ___|\    \|\    \ |\     \   ___|\     \   ___|\    \  
|    |       |     \     \  /    /\    \ |    |\    \\\    \| \     \ |     \     \ |    |\    \ 
|    |       |     ,_____/||    |  |    ||    | |    |\|    \  \     ||     ,_____/||    | |    |
|    |  ____ |     \--'\_|/|    |__|    ||    |/____/  |     \  |    ||     \--'\_|/|    |/____/ 
|    | |    ||     /___/|  |    .--.    ||    |\    \  |      \ |    ||     /___/|  |    |\    \ 
|    | |    ||     \____|\ |    |  |    ||    | |    | |    |\ \|    ||     \____|\ |    | |    |
|____|/____/||____ '     /||____|  |____||____| |____| |____||\_____/||____ '     /||____| |____|
|    |     |||    /_____/ ||    |  |    ||    | |    | |    |/ \|   |||    /_____/ ||    | |    |
|____|_____|/|____|     | /|____|  |____||____| |____| |____|   |___|/|____|     | /|____| |____|
  \(    )/     \( |_____|/   \(      )/    \(     )/     \(       )/    \( |_____|/   \(     )/  
   '    '       '    )/       '      '      '     '       '       '      '    )/       '     '   
                     '                                                        '  
        </pre>
        <p class="title-warning-text">Dont worry you are on the right page - dont run away and try typing "help"</p>
        <p class="title-ps-text">PS: this site is meant to look like this and you will soon see why</p>
        <hr class="title-hr">
    </div>
    <div class="main-container">
      <HomeCommandLine />
    </div>
</template>

<script setup>
import HomeCommandLine from '@/components/commandline/HomeCommandLine.vue'
import { onMounted } from 'vue'

// generates the random color for the title
onMounted(() => {
    const random = Math.floor(Math.random() * 5);
    const colors = ["dark:text-blue-600", "dark:text-green-600", "dark:text-red-600", "dark:text-orange-600", "dark:text-violet-600",];
    const ascii = document.getElementById("ascii-art")
    ascii.classList.add(colors[random])
})
</script>
