import { useEffect } from "react";

export default function useTaskStream(onMessage) {
  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/task/ws");

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data);
    };

    return () => socket.close();
  }, []);
}
