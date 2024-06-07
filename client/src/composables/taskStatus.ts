import { TaskStatus } from "@/interfaces/task";

const statusMap: Record<TaskStatus, { title: string; color: string }> = {
  queued: {
    title: "Queued",
    color: "bluegrey",
  },
  partial: {
    title: "Partial",
    color: "warning",
  },
  completed: {
    title: "Completed",
    color: "success",
  },
};

export default function useTaskStatus() {

  return {
    statusList: Object.keys(statusMap) as unknown as TaskStatus[],
    statusMap: statusMap
  }
}
