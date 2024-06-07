// Utilities
import { defineStore } from "pinia";

import { useWebSocketStore } from "./socket";

export const useAppStore = defineStore("app", () => {
  const socketStore = toRefs(useWebSocketStore());

  return {
    wsStatus: socketStore.status,
  };
});
