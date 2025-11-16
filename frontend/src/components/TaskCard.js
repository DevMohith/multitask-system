export default function TaskCard({ task }) {
  return (
    <div style={{ padding: 10, border: "1px solid black", margin: 10 }}>
      <b>Task:</b> {task.task_id} <br />
      <b>Type:</b> {task.type} <br />
      <b>Result:</b>
      <pre>{JSON.stringify(task.result, null, 2)}</pre>
    </div>
  );
}
