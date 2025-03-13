<template>
    <div class="navbar-bottom">
        <hr class="navbar-bottom-spliter mb-2">
        <div class="navbar-bottom-item-container">
            <div class="navbar-bottom-item dark:github-gradient">
                <h1>Github</h1>
            </div>
            <div class="navbar-bottom-item dark:premium-gradient" v-if="!premiumUser && localUser">
                <h1>Get Premium</h1>
            </div>
            <div class="navbar-bottom-item dark:instagram-gradient">
                <h1>Socials</h1>
            </div>
            <div class="navbar-bottom-item dark:license-gradient">
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