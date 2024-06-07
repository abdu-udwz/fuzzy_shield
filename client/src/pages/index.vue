<script lang="ts" setup>
import QueryForm from '@/components/QueryForm.vue';
import TaskCard from '@/components/TaskCard.vue';
import RecentTasks from '@/components/RecentTasks.vue';
</script>

<template>
  <VContainer class="fill-height">
    <VResponsive
      class="align-center gy-2 fill-height mx-auto"
    >

      <RecentTasks />
    </VResponsive>
  </VContainer>
</template>
