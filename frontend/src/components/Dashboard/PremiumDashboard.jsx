export default function PremiumDashboard({ stats }) {
  if (!stats.length) return <p>No data yet. Share your blog to get started!</p>;

  return (
    <div>
      <h2>Your Posts — Premium Analytics</h2>
      {stats.map((post) => (
        <div key={post.post_id} style={{ border: "1px solid #ccc", padding: "1rem", marginBottom: "1rem" }}>
          <h3>{post.title}</h3>

          <h4>Overview</h4>
          <p>👁 Views: <strong>{post.total_views}</strong></p>
          <p>👍 Likes: <strong>{post.total_likes}</strong></p>
          <p>💬 Comments: <strong>{post.total_comments}</strong></p>
          <p>🔗 Shares: <strong>{post.total_shares}</strong></p>

          <h4>Engagement</h4>
          <p>⏱ Avg Time Spent: <strong>{post.avg_time_spent_seconds}s</strong></p>
          <p>📜 Avg Scroll Depth: <strong>{post.avg_scroll_depth_percent}%</strong></p>

          <h4>Views Over Time</h4>
          {post.time_series.length ? (
            <table>
              <thead>
                <tr><th>Date</th><th>Views</th></tr>
              </thead>
              <tbody>
                {post.time_series.map((row) => (
                  <tr key={row.date}>
                    <td>{row.date}</td>
                    <td>{row.views}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : <p>No time series data yet</p>}

          <h4>Country Breakdown</h4>
          {post.country_breakdown.length ? (
            <ul>
              {post.country_breakdown.map((row) => (
                <li key={row.country}>{row.country}: {row.count} events</li>
              ))}
            </ul>
          ) : <p>No country data yet</p>}
        </div>
      ))}
    </div>
  );
}