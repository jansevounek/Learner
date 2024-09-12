<template>
    <div class="title-container">
        <pre class="ascii-container text-[5px] lg:text-[10px]" id="ascii-art1">                                     

          _          _    _        _         _   _         _            _           _       
        /\ \       / /\ /\ \     /\_\      /\_\/\_\ _    /\ \         /\ \     _  /\ \     
       /  \ \     / /  \\ \ \   / / /     / / / / //\_\ /  \ \       /  \ \   /\_\\_\ \    
      / /\ \ \   / / /\ \\ \ \_/ / /     /\ \/ \ \/ / // /\ \ \     / /\ \ \_/ / //\__ \   
     / / /\ \_\ / / /\ \ \\ \___/ /     /  \____\__/ // / /\ \_\   / / /\ \___/ // /_ \ \  
    / / /_/ / // / /  \ \ \\ \ \_/     / /\/________// /_/_ \/_/  / / /  \/____// / /\ \ \ 
   / / /__\/ // / /___/ /\ \\ \ \     / / /\/_// / // /____/\    / / /    / / // / /  \/_/ 
  / / /_____// / /_____/ /\ \\ \ \   / / /    / / // /\____\/   / / /    / / // / /        
 / / /      / /_________/\ \ \\ \ \ / / /    / / // / /______  / / /    / / // / /         
/ / /      / / /_       __\ \_\\ \_\\/_/    / / // / /_______\/ / /    / / //_/ /          
\/_/       \_\___\     /____/_/ \/_/        \/_/ \/__________/\/_/     \/_/ \_\/           
                                                                                           
        </pre>
        <pre class="ascii-container text-[5px] lg:text-[10px]" id="ascii-art2">
     _______. __    __    ______   ______  _______     _______.     _______. _______  __    __   __       __      
    /       ||  |  |  |  /      | /      ||   ____|   /       |    /       ||   ____||  |  |  | |  |     |  |     
   |   (----`|  |  |  | |  ,----'|  ,----'|  |__     |   (----`   |   (----`|  |__   |  |  |  | |  |     |  |     
    \   \    |  |  |  | |  |     |  |     |   __|     \   \        \   \    |   __|  |  |  |  | |  |     |  |     
.----)   |   |  `--'  | |  `----.|  `----.|  |____.----)   |   .----)   |   |  |     |  `--'  | |  `----.|  `----.
|_______/     \______/   \______| \______||_______|_______/    |_______/    |__|      \______/  |_______||_______|
                                                                                                                  
        </pre>
        <p class="title-warning-text">Enjoy your premium version of our app</p>
        <hr class="title-hr">
    </div>
    <div class="main-container">
        <p class="text-center text-green-500">Press enter to continue...</p>
    </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'

// import a setup of the router
import { useRouter } from 'vue-router'
const router = useRouter()

onUnmounted(() => {
    window.removeEventListener('keydown', handleKeyDown);
})

// generates the random color for the title
onMounted(() => {
    window.addEventListener('keydown', handleKeyDown);
    const random = Math.floor(Math.random() * 5);
    const colors1 = ["text-blue-600", "text-green-600", "text-red-600", "text-orange-600", "text-violet-600",];
    const colors2 = ["text-violet-600", "text-orange-600", "text-blue-600", "text-green-600", "text-red-600",];
    const ascii1 = document.getElementById("ascii-art1")
    const ascii2 = document.getElementById("ascii-art2")
    ascii1.classList.add(colors1[random])
    ascii2.classList.add(colors2[random])
})

function handleKeyDown(event) {
    if (event.key === "Enter") {
        router.push("/") 
    }
}
</script>