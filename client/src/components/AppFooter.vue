<script setup lang="ts">
import { useWebSocketStore } from '@/stores/socket';
import { mdiCircle } from '@mdi/js'

const socketStore = useWebSocketStore()

const socketIndictor = computed(() => socketStore.status === 'OPEN' ? 'success' : socketStore.status == 'CONNECTING' ? 'warning' : 'error')
</script>

<template>
  <VFooter
    height="40"
    app
    absolute
    style="bottom: 0; right: 0; left: 0;"
  >
    <span><VIcon
      :icon="mdiCircle"
      :color="socketIndictor"
    />&nbsp;Live updates </span>
  </VFooter>
</template>


<style scoped>
  .social-link :deep(.v-icon) {
    color: rgba(var(--v-theme-on-background), var(--v-disabled-opacity));
    text-decoration: none;
    transition: .2s ease-in-out;
  }
</style>
