export default function BasicDashboard({ stats }) {
  if (!stats.length) return <p>No data yet. Share your blog to get started!</p>;

  return (
    <div>
      <h2>Your Posts — Basic Analytics</h2>
      {stats.map((post) => (
        <div key={post.post_id} style={{ border: "1px solid #ccc", padding: "1rem", marginBottom: "1rem" }}>
          <h3>{post.title}</h3>
          <p>👁 Total Views: <strong>{post.total_views}</strong></p>
          <p>👍 Total Likes: <strong>{post.total_likes}</strong></p>
        </div>
      ))}
    </div>
  );
}