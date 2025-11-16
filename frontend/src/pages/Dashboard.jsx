import { useState } from "react";
import useTaskStream from "../hooks/useTaskStream";
import TaskCard from "../components/TaskCard";

export default function Dashboard() {
  const [tasks, setTasks] = useState([]);

  useTaskStream((message) => {
    setTasks((prev) => [...prev, message]);
  });

  async function createTask(type) {
    const payload = type === "research"
      ? "india population"
      : "x=10; y=20; z=x+y";

    await fetch(`http://localhost:8000/task/create?type=${type}&payload=${payload}`, {
      method: "POST"
    });
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Task Dashboard</h1>

      <button onClick={() => createTask("research")}>Run Research Task</button>
      <button onClick={() => createTask("python")}>Run Python Task</button>

      {tasks.map((task, index) => (
        <TaskCard key={index} task={task} />
      ))}
    </div>
  );
}
