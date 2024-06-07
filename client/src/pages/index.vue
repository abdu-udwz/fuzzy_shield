<script lang="ts" setup>
import TaskFormForm from '@/components/TaskForm.vue';
import TaskCard from '@/components/TaskCard.vue';
import RecentTasks from '@/components/RecentTasks.vue';
</script>

<template>
  <VContainer class="fill-height">
    <VResponsive
      class="align-center gy-2 fill-height mx-auto"
    >
      <TaskFormForm />

      <TaskCard class="my-2" />

      <RecentTasks />
    </VResponsive>
  </VContainer>
</template>
