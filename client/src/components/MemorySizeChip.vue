<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  modelValue: number | string;
}

const props = defineProps<Props>();

const formattedSize = computed(() => {
  const bytes = typeof props.modelValue === 'string' ? parseInt(props.modelValue, 10) : props.modelValue;
  if (isNaN(bytes)) return 'Invalid Size';

  const sizes = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
  if (bytes === 0) return '0 B';
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  const value = bytes / Math.pow(1024, i);
  return `${value.toFixed(2)} ${sizes[i]}`;
});
</script>

<template>
  <VChip variant="text">
    {{ formattedSize }}
  </VChip>
</template>

