import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";
import { useCollectionsStore } from "./collections";
import { useTasksStore } from "./tasks";
import { submitTask as apiSubmitTask } from "@/services/tasks";
import type { TaskStatus } from "@/interfaces/task";
import { type ScorerAlgorithm } from "@/composables/algorithms";

export const useTaskFormStore = defineStore("taskForm", () => {
  const collectionsStore = useCollectionsStore();
  const tasksStore = useTasksStore();

  const text = useLocalStorage("form.text", "");
  const collection = useLocalStorage("form.collection", "");
  const designatedResult = useLocalStorage("form.designatedResult", false);

  const attackType = useLocalStorage("form.attackType", ["sqli", "xss"]);

  const taskStatus: TaskStatus[] = ["queued", "partial", "completed"];
  const algorithmSelection = useLocalStorage<Record<ScorerAlgorithm, boolean>>(
    "form.selection",
    {
      hamming: true,
      naive: true,
      levenshtein_ratio: true,
      levenshtein_sort: true,
    }
  );

  const submitting = ref(false);
  async function submitTask() {
    const { data, error } = await apiSubmitTask({
      text: text.value,
      collection: collection.value,
      designated_result: designatedResult.value,

      sqli: attackType.value.includes("sqli"),
      xss: attackType.value.includes("xss"),

      hamming: algorithmSelection.value.hamming,
      naive: algorithmSelection.value.naive,
      levenshtein_ratio: algorithmSelection.value.levenshtein_ratio,
      levenshtein_sort: algorithmSelection.value.levenshtein_sort,
    });

    // refresh collections
    void collectionsStore.fetch();
    void tasksStore.fetchTasks();

    if (error.value) {
      throw error.value;
    }

    tasksStore.activeTask = data.value;
    text.value = "";
  }

  return {
    text,
    collection,
    designatedResult,
    attackType,

    algorithmSelection,

    taskStatus,

    submitting,
    submitTask,
  };
});
