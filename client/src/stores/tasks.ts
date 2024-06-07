import { defineStore } from "pinia";
import { getTasks, type GetTasksQueryParams } from '@/services/tasks'
import type { TaskRaw, TaskStatus, SocketUpdate } from '@/interfaces/task'
import { useLocalStorage } from "@vueuse/core";
import { useWebSocketStore } from "./socket";
export const useTasksStore = defineStore('tasks', () => {
  const socket = useWebSocketStore()

  const activeTask = ref<TaskRaw | null>(null)

  const tasks = ref<TaskRaw[]>([])
  const taskCount = ref<number>(10)
  const loading = ref(false)

  const status = ref<TaskStatus | null>(null)
  const collection = ref<string | null>(null)
  const page = ref(1)
  const pageLength = useLocalStorage('tasks.pageLength', 10)

  async function fetchTasks() {
    const filters: GetTasksQueryParams = {
      limit: pageLength.value,
      page: page.value -1,
    }
    if (status.value) {
      filters.status = status.value
    }
    if (collection.value != null && collection.value.trim()) {
      filters.collection = collection.value.trim()
    }
    loading.value = true
    const { data } = await getTasks(filters)
    if (data.value != null) {
      tasks.value = data.value.tasks
      taskCount.value = data.value.count
    }
    loading.value = false
  }

  watch([status, collection, page, pageLength], async() => {
    await fetchTasks()
  }, {immediate: true})

  watch(() => socket.data, (data) => {
    if (data == null) {
      return
    }
    console.info("[Socket]:", data)

    try {
      const update = JSON.parse(data) as SocketUpdate

      if (activeTask.value?.task_id == update.task_id) {
          Object.assign(activeTask.value, update)
      }
      for (const task of tasks.value) {
        if (task.task_id === update.task_id) {
          Object.assign(task, update)
        }
      }

    } catch (error: any) {
      console.error('[tasks]: an error occurred while parsing socket update json')
    }
  })

  return {
    activeTask,

   tasks,
   taskCount,
   loading,

   status,
   collection,

   page,
   pageLength,
  }
})
