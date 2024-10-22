<template>
    <div class="navbar-top">
        <div class="navbar-top-item-container">
            <div class="navbar-top-item text-orange-500" v-if="currentRoute !== '/' && !isWithoutCmd">
                <h1>1</h1>
                <h1>Home</h1>
            </div>
            <div class="navbar-top-item text-blue-500" v-if="currentRoute !== '/login' && !localUser && !isWithoutCmd">
                <h1>2</h1>
                <h1>Login</h1>
            </div>
            <div class="navbar-top-item text-red-500" v-if="currentRoute !== '/signup' && !localUser && !isWithoutCmd">
                <h1>3</h1>
                <h1>Signup</h1>
            </div>
            <div class="navbar-top-item text-purple-500" v-if="currentRoute == '/' && !isWithoutCmd">
                <h1>4</h1>
                <h1>About us</h1>
            </div>
            <div class="navbar-top-item text-pink-500" v-if="!localUser && currentRoute !== '/resetpassword' && !isWithoutCmd">
                <h1>5</h1>
                <h1>Forgot Password?</h1>
            </div>
            <div class="navbar-top-item text-green-500" v-if="localUser && !isWithoutCmd">
                <h1>6</h1>
                <h1>Logout</h1>
            </div>
            <div class="navbar-top-item rainbow-text" v-if="localUser && currentRoute !== '/learning/homepage' && currentRoute !== '/learning/lessons' && !isWithoutCmd">
                <h1>7</h1>
                <h1>Lets Learn</h1>
            </div>
            <div class="navbar-top-item text-red-500" v-if="localUser && currentRoute !== '/learning/homepage' && currentRoute !== '/learning/admin' && !isWithoutCmd">
                <h1>8</h1>
                <h1>Admin</h1>
            </div>
            <div class="navbar-top-item text-red-500" v-if="localUser && isWithoutCmd">
                <h1>Use ctrl + c</h1>
                <h1>to go back</h1>
            </div>
        </div>
        <hr class="navbar-top-spliter mt-2">
    </div>
</template>


<script setup>
import { computed, ref, onMounted } from 'vue'
import { supabase } from '@/supabase/init.js'

// router import a setup
import { useRoute } from 'vue-router'
const route = useRoute()

const localUser = ref(false)

// credit https://stackoverflow.com/questions/53926267/dynamically-show-components-depending-on-the-current-route-vuejs
// returns the current path
const currentRoute = computed(() => {
    return route.path
})

const isWithoutCmd = computed(() => {
    const regex1 = /^\/container\/\d+$/;
    const regex2 = /^\/learning\/container\/\d+$/;
    if (regex1.test(currentRoute.value) 
        || currentRoute.value === '/learning/lections'
        || regex2.test(currentRoute.value)){
        return true
    }
    return false
})

async function getUser() {
    const { data: { user } } = await supabase.auth.getUser()
    if (user) {
        localUser.value = true
    } else {
        localUser.value = false
    }
}


onMounted(() => {
    getUser()
})
</script>

<style>
.rainbow-text {
    background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);
    background-clip: text;
    -webkit-background-clip: text;
    color: transparent;
}
</style>