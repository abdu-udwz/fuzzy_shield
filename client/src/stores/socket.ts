import { useWebSocket } from "@vueuse/core";
import { defineStore } from "pinia";
export const useWebSocketStore = defineStore("websocket", () => {
  const s = useWebSocket<string>(`ws://${window.location.host}/api/ws/`, {
    autoClose: true,
    onConnected(ws) {
      console.log("Socket connection established");
    },
    onDisconnected(ws, event) {
      console.log("socket disconnected", event);
    },
    onError(ws, event) {
      console.log("socket error", console.error);
    },
    autoReconnect: {
      retries: 3,
      onFailed() {
        console.error("There was an error reconnecting socket after 3 retries");
        console.log(s.status.value);
        console.log(s.ws.value);
      },
    },
    // heartbeat: {
    //   message: 'ping',
    //   interval: 20000,
    //   pongTimeout: 20000,
    // },
  });

  return s;
});
