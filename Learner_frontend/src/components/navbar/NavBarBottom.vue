<template>
    <div class="navbar-bottom">
        <hr class="navbar-bottom-spliter mb-2">
        <div class="navbar-bottom-item-container">
            <div class="navbar-bottom-item github-gradient-text">
                <h1>Github</h1>
            </div>
            <div class="navbar-bottom-item premium-gradient-text" v-if="!premiumUser && localUser">
                <h1>Get Premium</h1>
            </div>
            <div class="navbar-bottom-item instagram-gradient-text">
                <h1>Socials</h1>
            </div>
            <div class="navbar-bottom-item license-gradient-text">
                <h1>License</h1>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getUser, getUserExtra } from '@/supabase/getFunctions.js'

let premiumUser = ref(false)

let localUser = ref(false)

async function setUser() {
    const user = await getUser()
    if (user) {
        getPremiumStatus()
        localUser.value = true
    } else {
        premiumUser.value = false
    }
}

async function getPremiumStatus() {
    const extra = await getUserExtra()
    if (extra) {
        premiumUser.value = extra[0].premium
    } else {
        console.log("an error when getting user extras for bottom navbar occured")
    }
}


onMounted(() => {
    setUser()
})
</script>

<style>
.instagram-gradient-text {
    background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.github-gradient-text {
    background: linear-gradient(90deg, #6e5494 0%, #8a63d2 50%);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.license-gradient-text {
    background: linear-gradient(90deg, #1e3a8a 0%, #10b981 100%);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.premium-gradient-text {
    background: linear-gradient(90deg, #ffd700 0%, #ffffff 100%);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>