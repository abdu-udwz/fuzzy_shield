<template>
  <VApp>
    <VMain>
      <RouterView />
    </VMain>
  </VApp>
</template>

<script lang="ts" setup>
import { useCollectionsStore } from '@/stores/collections'

useCollectionsStore()

//
</script>
