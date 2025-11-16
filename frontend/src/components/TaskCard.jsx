export default function TaskCard({ task }) {
  return (
    <div style={{
      padding: 15,
      border: "1px solid #ccc",
      borderRadius: 8,
      margin: "15px 0",
      background: "#fafafa"
    }}>

      <h3>{task.type.toUpperCase()} RESULT</h3>
      <p><b>Query:</b> {task.query}</p>

      {/* Summary */}
      {task.summary && (
        <div>
          <h4>Summary</h4>
          <p>{task.summary}</p>
        </div>
      )}

      {/* Links */}
      {task.links && task.links.length > 0 && (
        <div>
          <h4>Web Results</h4>
          <ul>
            {task.links.map((link, i) => (
              <li key={i}>
                <a href={link.url} target="_blank" rel="noopener noreferrer">
                  {link.title}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Images */}
      {task.images && task.images.length > 0 && (
        <div>
          <h4>Images</h4>
          <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
            {task.images.slice(0, 6).map((img, i) => (
              <img
                key={i}
                src={img.thumbnail || img.image}
                alt={img.title}
                width="120"
                style={{ borderRadius: 6 }}
              />
            ))}
          </div>
        </div>
      )}

      {/* Videos */}
      {task.videos && task.videos.length > 0 && (
        <div>
          <h4>Videos</h4>
          <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
            {task.videos.slice(0, 4).map((vid, i) => (
              <div key={i} style={{ maxWidth: 240 }}>
                <a href={vid.url} target="_blank" rel="noopener noreferrer">
                  <img
                    src={vid.thumbnail}
                    alt={vid.title}
                    width="230"
                    style={{ borderRadius: 6 }}
                  />
                </a>
                <p>{vid.title}</p>
              </div>
            ))}
          </div>
        </div>
      )}

    </div>
  );
}
