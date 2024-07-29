<template>
    <p>Hello</p>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useRoute } from 'vue-router'
import { supabase } from '../../supabase/init.js'

const route = useRoute()
const router = useRouter()
const lection = ref([])

onMounted(() => {
    getLesson()
})


async function getLesson() {
    const { data, error } = await supabase
        .from("lections")
        .select("*")
        .eq("id", route.params.id)
    
    if(error){
        router.push('/learning/lections')
    }

    if (data.length == 1) {
        lection.value = await data
        console.log(lection.value)
    } else {
        router.push('/learning/lections')
    }
}
</script>