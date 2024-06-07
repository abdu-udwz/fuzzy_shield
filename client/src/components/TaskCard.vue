<script setup lang="ts">
import useTaskStatus from '@/composables/taskStatus';
import { useTasksStore } from '@/stores/tasks';
import { mdiClose } from '@mdi/js';

const tasksStore = useTasksStore()

const {  statusMap } = useTaskStatus()

const activeTask = computed(() => tasksStore.activeTask)

const showMoreButton = computed(() => activeTask.value && activeTask.value.text.length > 70)
const displayedText = computed(() => {
  if (!showMoreButton.value) {
    return activeTask.value?.text
  }

  return activeTask.value?.text.substring(0, 57) + '...'
})

const textDialog = ref(false)

</script>

<template>
  <VExpandTransition>
    <VCard v-if="activeTask != null">
      <VCardText>
        <VRow>
          <!-- info col -->
          <VCol md="2">
            <VDefaultsProvider
              :defaults="{ global: { density: 'compact'}}"
            >
              <VCard
                flat
                class="d-flex flex-column h-100"
              >
                <VCardTitle class="pb-0">
                  Task Details
                </VCardTitle>
                <VCardSubtitle class="px-2 pa-0">
                  <VChip
                    size="small"
                    label
                    variant="plain"
                  >
                    {{ new Date(activeTask.created_at+'Z').toLocaleDateString() }} {{ new Date(activeTask.created_at+'Z').toLocaleTimeString() }}
                  </VChip>
                  <br />
                  <VChip
                    size="small"
                    label
                    variant="plain"
                  >
                    #{{ activeTask.collection }}
                  </VChip>
                </VCardSubtitle>
                <VCardText
                  class="flex-grow-1 py-0"
                  style="min-height: 0;"
                >
                  <VChip
                    size="small"
                    variant="flat"
                    label
                    :color="statusMap[activeTask.status].color"
                  >
                    {{ statusMap[activeTask.status].title }}
                  </VChip>

                  <section class="mt-2 ">
                    <h6>
                      Text
                    </h6>
                    <p class="pa-1 bg-surface-light rounded text-caption">
                      {{ displayedText }}
                      <a
                        v-if="showMoreButton"
                        href="javascript:;"
                        @click="textDialog = true"
                      >
                        Show more
                      </a>
                    </p>
                  </section>
                </VCardText>
                <VCardActions>
                  <VBtn
                    block
                    size="small"
                    variant="plain"
                    :prepend-icon="mdiClose"
                    @click="tasksStore.activeTask = null"
                  >
                    Hide Details
                  </VBtn>
                </VCardActions>
              </VCard>
            </VDefaultsProvider>
          </VCol>
          <!-- sqli column -->
          <VCol md="5">
            <VCard
              flat
              :disabled="!activeTask?.sqli"
            >
              <VCardTitle class="text-subtitle-1">
                <span>SQLi</span> <span v-show="!activeTask?.sqli">(Not enabled)</span>
              </VCardTitle>
              <TaskResultGrid
                :model-value="activeTask"
                :disabled="!activeTask?.sqli"
              />
            </VCard>
          </VCol>
          <!-- xss column -->
          <VCol md="5">
            <VCard
              flat
              :disabled="!activeTask?.xss"
            >
              <VCardTitle class="text-subtitle-1">
                <span>XSS</span> <span v-show="!activeTask?.xss">(Not enabled)</span>
              </VCardTitle>
              <TaskResultGrid
                :model-value="activeTask"
                :disabled="!activeTask?.xss"
                xss
              />
            </VCard>
          </VCol>
        </VRow>
      </VCardText>


      <VDialog
        v-model="textDialog"
        width="70vw"
      >
        <VCard>
          <VCardTitle>Task Text</VCardTitle>
          <VCardText>
            {{ activeTask.text }}
          </VCardText>
          <VCardActions>
            <VSpacer />
            <VBtn
              variant="flat"
              color="primary"
              @click="textDialog = false"
            >
              Close
            </VBtn>
          </VCardActions>
        </VCard>
      </VDialog>
    </VCard>
  </VExpandTransition>
</template>
