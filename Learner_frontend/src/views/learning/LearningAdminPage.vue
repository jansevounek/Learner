<template>
    <div class="title-container">
      <p class="title-warning-text">Here you can create teams for your students and lessons</p>
      <p class="title-ps-text">PS: you have a limit of two teams</p>
      <hr class="title-hr">
    </div>
    <div class="main-container">
      <AdminCommandLine />
    </div>
  </template>
  
  <script setup>
  import AdminCommandLine from '@/components/commandline/learning/AdminCommandLine.vue'
  </script>