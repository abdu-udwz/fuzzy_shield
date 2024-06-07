<script setup lang="ts">

const props = defineProps<{
  modelValue: string | number
}>()

const displayValue = computed(() => {
  const value = typeof props.modelValue === 'string' ? parseFloat(props.modelValue) : props.modelValue
  if (value === 0 || Number.isNaN(value)) {
    return "N/A"
  }

  if (value >= 1000) {
    // seconds
    return (value/1000).toFixed(1) + 'sec'
  } else if (value >= 60 * 1000) {
    // minutes
    return (value/ (1000 * 60)).toFixed(1) + 'min'
  } else if (value > 1 && value < 1000) {
    // milli
    return value.toFixed(1) + 'ms'
  } else if (value < 1) {
    // micro
    return (value * 100).toFixed(1) + 'us'
  }
})

</script>

<template>
  <VChip
    size="small"
    variant="text"
    v-bind="$attrs"
  >
    {{ displayValue }}
  </VChip>
</template>
