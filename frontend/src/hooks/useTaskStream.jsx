import { useEffect, useState } from "react";

export default function useTaskStream() {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/task/ws");

    ws.onopen = () => console.log("WS Connected!");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log("WS MSG:", data);  
      setMessages((prev) => [data, ...prev]);
    };

    ws.onerror = (err) => console.error("WS Error:", err);

    return () => ws.close();
  }, []);

  return messages;
}
