<script setup lang="ts">
// You might choose this based on an API call or logged-in status
const layout = 'custom';
</script>

<template>
  <div>
    <NuxtLayout :name="layout">
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>
