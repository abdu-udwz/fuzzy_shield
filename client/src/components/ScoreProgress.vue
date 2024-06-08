<script setup lang="ts">
const props = defineProps<{
  modelValue?: number | null;
}>();

// const color = computed(() => {

// })

const color = computed(() => {
  if (!props.modelValue || props.modelValue == 0) {
    return undefined
  }

  const red = Math.round((props.modelValue / 100) * 255);
  const green = Math.round((1 - props.modelValue / 100) * 255);
  const blue = 0;

  const toHex = (v: number) => v.toString(16).padStart(2, "0");

  return `#${toHex(red)}${toHex(green)}${toHex(blue)}`;
});

const formattedValue = computed(() => {
  if (props.modelValue == null || Number.isNaN(props.modelValue) || props.modelValue === -1) {
    return undefined
  }


  return props.modelValue.toFixed(0)
})
</script>

<template>
  <VProgressCircular
    width="2"
    size="small"
    :color="color"
    :model-value="modelValue == null || Number.isNaN(modelValue) ? undefined : modelValue"
    v-bind="$attrs"
  >
    <span
      v-if="modelValue != null"
      class="text-caption"
      style="font-size: 7pt"
    >
      {{ formattedValue }}
    </span>
  </VProgressCircular>
</template>
