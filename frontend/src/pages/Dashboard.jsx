import React from "react";
import useTaskStream from "../hooks/useTaskStream";

export default function Dashboard() {
  const results = useTaskStream();  // <---- USE THE HOOK

  const createTask = async (type) => {
    const payload =
      type === "research"
        ? "india population"
        : "x=10; y=20; z=x+y";

    await fetch(
      `http://localhost:8000/task/create?type=${type}&payload=${payload}`,
      {
        method: "POST",
      }
    );
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Task Dashboard</h1>

      <button onClick={() => createTask("research")}>Run Research Task</button>
      <button onClick={() => createTask("python")}>Run Python Task</button>

      <h2>Results:</h2>

      {results.map((task, i) => (
        <div
          key={i}
          style={{
            padding: 10,
            marginTop: 10,
            border: "1px solid #888",
            borderRadius: 8,
          }}
        >
          <h3>{task.type?.toUpperCase()} RESULT</h3>
          <pre>{JSON.stringify(task, null, 2)}</pre>
        </div>
      ))}
    </div>
  );
}
