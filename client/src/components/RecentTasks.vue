<script setup lang="ts">
import { useCollectionsStore } from "@/stores/collections";
import useAlgorithms from "@/composables/algorithms";
import { useTasksStore } from "@/stores/tasks";

import { formatTimeAgo } from '@vueuse/core'
import useTaskStatus from "@/composables/taskStatus";
import { VDataTableServer } from "vuetify/components";

const collectionsStore = useCollectionsStore();

const tasksStore = useTasksStore();

const headers = ref([
  {
    title: "Text",
    align: "start",
    sortable: false,
    key: "text",
  },
  { title: "Status", key: "status", align: "center", sortable: false },
  {
    title: "SQLi",
    key: "sqli",
    align: "center",
    sortable: false,
    children: [
      {
        title: "H.",
        key: "hamming_sqli_score",
        align: "center",
        sortable: false,
      },
      {
        title: "N.",
        key: "naive_sqli_score",
        align: "center",
        sortable: false,
      },
      {
        title: "L.R.",
        key: "levenshtein_ratio_sqli_score",
        align: "center",
        sortable: false,
      },
      {
        title: "L.S.",
        key: "levenshtein_sort_sqli_score",
        align: "center",
        sortable: false,
      },
    ],
  },
  {
    key: 'spacer',
    width: '6px',
    sortable: false,
  },
  {
    title: "XSS",
    key: "xss",
    align: "center",
    sortable: false,
    children: [
      {
        title: "H.",
        key: "hamming_xss_score",
        sortable: false,
        align: "center",
      },
      {
        title: "N.",
        key: "naive_xss_score",
        sortable: false,
        align: "center",
      },
      {
        title: "L.R.",
        key: "levenshtein_ratio_xss_score",
        sortable: false,
        align: "center",
      },
      {
        title: "L.S.",
        key: "levenshtein_sort_xss_score",
        sortable: false,
        align: "center",
      },
    ],
  },
  { title: "Date", key: "created_at", sortable: false },
] as any);

const { statusList: taskStatus, statusMap } = useTaskStatus();

const statusOptions = computed(() => {
  return taskStatus.map((status) => ({
    title: status,
    value: status,
  }));
});

function onRowClicked(event: PointerEvent, payload: any) {
  tasksStore.activeTask = payload.item;
}

const {algorithms} = useAlgorithms()

type ScoreKey = `${keyof typeof algorithms}_${"sqli" | "xss"}_score`

const scoreKeys: ScoreKey[] = [] ;
(['sqli', 'xss'] as const).forEach(attack => {
  Object.keys(algorithms).forEach((algo) => {
    scoreKeys.push(`${algo}_${attack}_score` as unknown as ScoreKey)
  })
})


function getSlotName(scoreProp: string) {
  // eslint-disable-next-line @typescript-eslint/no-unnecessary-type-assertion
  return `item.${scoreProp}`  as `item.${string}`
}
</script>

<template>
  <VCard
    class="mt-2"
    title="Search tasks"
  >
    <VCardText>
      <VDataTableServer
        v-model:items-per-page="tasksStore.pageLength"
        v-model:page="tasksStore.page"
        :items-length="tasksStore.taskCount"
        :items="tasksStore.tasks"
        item-value="task_id"
        :headers="headers"
        :loading="tasksStore.loading"
        hover
        sticky
        fixed-footer
        fixed-header
        @click:row="onRowClicked"
      >
        <template #top>
          <VRow dense>
            <VCol md="8">
              <VCombobox
                v-model="tasksStore.collection"
                label="Collection"
                clearable
                :items="collectionsStore.collections"
              />
            </VCol>
            <VCol md="4">
              <VSelect
                v-model="tasksStore.status"
                label="Status"
                :items="statusOptions"
                clearable
              />
            </VCol>
          </VRow>
        </template>

        <template #item.status="{ item }">
          <VChip
            :color="statusMap[item.status].color"
            class="text-capitalize"
          >
            {{ statusMap[item.status].title }}
          </VChip>
        </template>

        <!-- eslint-ignore -->
        <template
          v-for="scoreKey in scoreKeys"
          :key="scoreKey"
          #[getSlotName(scoreKey)]="{item}"
        >
          <ScoreProgress :model-value="item[scoreKey]" />
        </template>

        <template #item.created_at="{ item }">
          {{ formatTimeAgo(new Date(item.created_at + ""), { showSecond: true}) }}
        </template>
      </VDataTableServer>
    </VCardText>
  </VCard>
</template>
