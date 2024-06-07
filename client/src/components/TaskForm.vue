<script setup lang="ts">
import { useTaskFormStore } from "@/stores/taskForm";
import { useCollectionsStore } from "@/stores/collections";
import {
  mdiBug,
  mdiDatabase,
  mdiLanguageJavascript,
  mdiShieldPlus,
} from "@mdi/js";

const taskForm = useTaskFormStore();
const collectionsStore = useCollectionsStore();
</script>

<template>
  <VCard
    :loading="taskForm.submitting"
    :disabled="taskForm.submitting"
  >
    <VForm>
      <VCardText>
        <VRow>
          <VCol md="9">
            <VTextField
              v-model="taskForm.text"
              label="Query"
              placeholder="Enter query to be tested here"
              variant="solo-filled"
              flat
            />
            <h6 class="ms-1 text-caption">
              Algorithm Selection
            </h6>
            <div class="d-flex">
              <VCheckbox
                v-model="taskForm.algorithmSelection.hamming"
                label="Hamming Distance"
                hide-details
              />
              <VCheckbox
                v-model="taskForm.algorithmSelection.naive"
                label="Naive Algorithm"
                hide-details
              />
              <VCheckbox
                v-model="taskForm.algorithmSelection.levenshtein_ratio"
                label="Levenshtein Ratio"
                hide-details
              />
              <VCheckbox
                v-model="taskForm.algorithmSelection.levenshtein_sort"
                label="Levenshtein Sort"
                hide-details
              />
            </div>
          </VCol>
          <VCol md="3">
            <VCombobox
              v-model="taskForm.collection"
              label="Collection"
              :items="collectionsStore.collections"
              variant="solo-filled"
              clearable
              flat
            />
            <!-- designated result  -->
            <VBtnToggle
              v-model="taskForm.designatedResult"
              variant="outlined"
              class="w-100 gx-2"
              divided
              density="compact"
            >
              <VBtn
                class="w-50"
                :value="true"
                :prepend-icon="mdiBug"
              >
                Malicious
              </VBtn>
              <VBtn
                class="w-50"
                :value="false"
                :prepend-icon="mdiShieldPlus"
              >
                Safe
              </VBtn>
            </VBtnToggle>

            <VBtnToggle
              v-model="taskForm.attackType"
              multiple
              mandatory
              variant="outlined"
              class="mt-2 w-100 gx-2"
              divided
              density="compact"
            >
              <VBtn
                class="w-50"
                value="sqli"
                :prepend-icon="mdiDatabase"
              >
                SQLi
              </VBtn>
              <VBtn
                class="w-50"
                value="xss"
                :prepend-icon="mdiLanguageJavascript"
              >
                XSS
              </VBtn>
            </VBtnToggle>
          </VCol>
        </VRow>
      </VCardText>
      <VCardActions>
        <VBtn
          variant="flat"
          color="primary"
          block
          @click="taskForm.submitTask"
        >
          Submit Task
        </VBtn>
      </VCardActions>
    </VForm>
  </VCard>
</template>
