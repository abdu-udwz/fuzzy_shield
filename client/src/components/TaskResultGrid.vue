<script setup lang="ts">
import TimeChip from './TimeChip.vue';
import useAlgorithms, { type ScorerAlgorithm, type ScorerAlgorithmProperty} from '@/composables/algorithms'
import ScoreProgress from './ScoreProgress.vue';

import { TaskRaw } from '@/interfaces/task';
import { mdiChip, mdiMemory, mdiTimerOutline } from '@mdi/js';

const props = defineProps<{
  modelValue: TaskRaw
  disabled?: boolean
  xss?: boolean
}>()

const task = computed(() => props.modelValue)


const {algorithms: rawAlgorithms} = useAlgorithms()

const algorithms = computed(() => Object.keys(rawAlgorithms) as unknown as ScorerAlgorithm[])

interface AlgorithmData {
  score: number
  time: number
  cpu: number
  memory: number
  match?: string
  class?: Record<string, any> | string[]
}

const displayResult = computed(() => {
  const algoValuesMap: Map<ScorerAlgorithm, AlgorithmData> = new Map()

  for (const algo  of algorithms.value) {
    const disabled = isAlgorithmDisabled(algo)

    algoValuesMap.set(algo, {
      score: getPropertyValue(algo, 'score'),
      time: getPropertyValue(algo, 'time'),
      cpu: getPropertyValue(algo, 'cpu'),
      memory: getPropertyValue(algo, 'memory'),
      class: disabled? ["text-disabled"] : undefined
    })
  }

  return algoValuesMap
})

function getPropertyValue(algo: ScorerAlgorithm, property:ScorerAlgorithmProperty ): number {
  if (props.disabled) {
    return NaN
  }

  const prefix = `${algo}_${props.xss ? 'xss' : 'sqli'}_` as const
  const propertyKey = `${prefix}${property}` as const
  let value =task.value[propertyKey] as unknown as number
  if (value === -1) {
    value = NaN
  }
  return value
}

function isAlgorithmDisabled(algo: ScorerAlgorithm):boolean {
  return !task.value[algo]
}

// match text dialog
const topMatchDialog = ref(false)
const topMatchAlgorithm = ref<ScorerAlgorithm | null>()

function showTopMatchDialog(algo: ScorerAlgorithm) {
  topMatchAlgorithm.value = algo
  topMatchDialog.value = true
}

</script>

<template>
  <VTable
    class="task-result-grid"
  >
    <thead>
      <tr>
        <th style="max-width: 0.1em;" />
        <th
          v-for="value, key in rawAlgorithms"
          :key="key"
          style="width: 20%;"
          :class="displayResult.get(key)?.class"
        >
          {{ value }}
        </th>
      </tr>
    </thead>
    <tbody>
      <!-- score row -->
      <tr>
        <td style="max-width: 10px;" />
        <td
          v-for="algo in algorithms"
          :key="algo"
          :class="displayResult.get(algo)?.class"
        >
          <ScoreProgress
            :indeterminate="!disabled && !isAlgorithmDisabled(algo) && !displayResult.get(algo)?.time"
            :model-value="disabled ? null : displayResult.get(algo)?.score"
            @click="showTopMatchDialog(algo)"
          />
        </td>
      </tr>
      <!-- time row -->
      <tr>
        <td>
          <VIcon :icon="mdiTimerOutline" />
        </td>
        <td
          v-for="algo in algorithms"
          :key="algo"
          :class="displayResult.get(algo)?.class"
        >
          <TimeChip :model-value="displayResult.get(algo)?.time ?? 0" />
        </td>
      </tr>
      <!-- cpu score -->
      <tr>
        <td>
          <VIcon :icon="mdiChip" />
        </td>
        <td
          v-for="algo in algorithms"
          :key="algo"
          :class="displayResult.get(algo)?.class"
        >
          <span
            v-if="!Number.isNaN(displayResult.get(algo)?.cpu)"
          >
            {{ displayResult.get(algo)?.cpu ?.toFixed(2) }}

            <span class="text-overline">%</span>
          </span>
          <span v-else>N/A</span>
        </td>
      </tr>
      <!-- memory usage  -->
      <tr>
        <td>
          <VIcon :icon="mdiMemory" />
        </td>
        <td
          v-for="algo in algorithms"
          :key="algo"
          :class="displayResult.get(algo)?.class"
        >
          <MemorySizeChip
            v-if="displayResult.get(algo)?.memory"
            :model-value="displayResult.get(algo)?.memory ?? 0"
          />
          <span v-else>N/A</span>
        </td>
      </tr>
    </tbody>
  </VTable>

  <VDialog v-model="topMatchDialog" width="70em">
    <VCard>
      <VCardTitle>{{ topMatchAlgorithm }}</VCardTitle>
      <VCardText>Top matching result: <br> {{ topMatchAlgorithm == null ? null : getPropertyValue(topMatchAlgorithm, 'match') }}</VCardText>
      <VCardActions>
        <VSpacer></VSpacer>
        <VBtn @click="topMatchDialog = false">Close</VBtn>
      </VCardActions>
    </VCard>
  </VDialog>
</template>


<style>
.task-result-grid th,
.task-result-grid td {
  text-align: center;
}

.task-result-grid tr th,
.task-result-grid tr td {
  padding: 0 4px 0 !important;
}

</style>
