export default function PremiumDashboard({ stats }) {
  if (!stats.length) return (
    <div className="empty-state">
      <p>No posts yet.</p>
      <a href="/create-post" className="btn btn-primary">
        Create your first post
      </a>
    </div>
  );

  return (
    <div>
      <div className="section-header">
        <h2>Your Posts</h2>
        <small>{stats.length} post{stats.length !== 1 ? "s" : ""}</small>
      </div>

      <div className="card-grid">
        {stats.map((post) => (
          <div key={post.post_id} className="card">
            <h3 className="post-card-title">{post.title}</h3>

            <div className="stat-grid">
              <div className="stat-box">
                <div className="stat-value">{post.total_views}</div>
                <div className="stat-label">👁 Views</div>
              </div>
              <div className="stat-box">
                <div className="stat-value">{post.total_likes}</div>
                <div className="stat-label">👍 Likes</div>
              </div>
              <div className="stat-box">
                <div className="stat-value">{post.total_comments}</div>
                <div className="stat-label">💬 Comments</div>
              </div>
              <div className="stat-box">
                <div className="stat-value">{post.total_shares}</div>
                <div className="stat-label">🔗 Shares</div>
              </div>
            </div>

            <div className="divider" />

            <h4>Engagement</h4>
            <div className="stat-grid" style={{ marginTop: "0.75rem" }}>
              <div className="stat-box">
                <div className="stat-value">{post.avg_time_spent_seconds}s</div>
                <div className="stat-label">⏱ Avg Time</div>
              </div>
              <div className="stat-box">
                <div className="stat-value">{post.avg_scroll_depth_percent}%</div>
                <div className="stat-label">📜 Avg Scroll</div>
              </div>
            </div>

            {post.time_series.length > 0 && (
              <>
                <div className="divider" />
                <h4>Views Over Time</h4>
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Views</th>
                    </tr>
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
              </>
            )}

            {post.country_breakdown.length > 0 && (
              <>
                <div className="divider" />
                <h4>Country Breakdown</h4>
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Country</th>
                      <th>Events</th>
                    </tr>
                  </thead>
                  <tbody>
                    {post.country_breakdown.map((row) => (
                      <tr key={row.country}>
                        <td>{row.country}</td>
                        <td>{row.count}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}