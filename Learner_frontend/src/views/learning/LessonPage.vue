<template>
    <div class="main-container">
        <div class="split-container">
            <div class="control-container">
                <LessonPageSelector />
            </div>
            <div class="linux-container">
                <button class="linux-button">Start Container</button>
                <!--<iframe :src="url" width="100%" height="100%" frameborder="0" class="practice-cmd"></iframe>-->
            </div>
        </div>
    </div>
</template>

<script setup>
import LessonPageSelector from '@/components/selector/learning/LessonPageSelector.vue'

let url = "https://youtube.com"
</script>