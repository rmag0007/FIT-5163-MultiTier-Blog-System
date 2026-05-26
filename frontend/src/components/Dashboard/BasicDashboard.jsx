export default function BasicDashboard({ stats }) {
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
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}