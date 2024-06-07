import { ScorerAlgorithm } from "@/composables/algorithms";
import { useAPI } from "./api";
import type { TaskRaw, TaskStatus } from "@/interfaces/task";
export type SubmitTaskForm = Pick<TaskRaw, 'text' | 'collection' | 'designated_result' | 'sqli' | 'xss' | ScorerAlgorithm>
export function submitTask(task: SubmitTaskForm) {
  return useAPI('tasks/').json<TaskRaw>().post(task)
}

export interface GetTasksQueryParams {
  collection?: string
  status?: TaskStatus
  limit?: number
  page?: number
  [key: string]: any
}
export function getTasks(params?: GetTasksQueryParams) {
  const p = params != null ? new URLSearchParams(params).toString() : ''
  // console.log(p)
  return useAPI(`/tasks?${p}`).json<{tasks: TaskRaw[], count: number}>().get()
}
