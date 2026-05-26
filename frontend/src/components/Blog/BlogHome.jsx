import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import client from "../../api/client";

export default function BlogHome() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  const username = localStorage.getItem("username");

  useEffect(() => {
    client.get("/posts")
      .then((res) => setPosts(res.data))
      .catch(() => setPosts([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="page">
      <nav className="navbar">
        <div className="navbar-inner">
          <a href="/" className="navbar-brand">
            Dev<span>Blog</span>
          </a>
          <div className="navbar-actions">
            {token ? (
              <>
                <span className="navbar-user">Hi, {username}</span>
                <button
                  className="btn btn-secondary btn-sm"
                  onClick={() => navigate("/dashboard")}
                >
                  Dashboard
                </button>
              </>
            ) : (
              <>
                <button
                  className="btn btn-ghost btn-sm"
                  onClick={() => navigate("/login")}
                >
                  Login
                </button>
                <button
                  className="btn btn-primary btn-sm"
                  onClick={() => navigate("/register")}
                >
                  Register
                </button>
              </>
            )}
          </div>
        </div>
      </nav>

      <div className="container">
        <div className="home-hero">
          <h1>Stories worth reading</h1>
          <p>Discover posts from developers, writers, and thinkers.</p>
        </div>

        <div className="section-header">
          <h2>Latest Posts</h2>
          {token && (
            <button
              className="btn btn-primary btn-sm"
              onClick={() => navigate("/create-post")}
            >
              + New Post
            </button>
          )}
        </div>

        {loading && <div className="loading">Loading posts...</div>}

        {!loading && posts.length === 0 && (
          <div className="empty-state">
            <p>No posts yet. Be the first to write one!</p>
            {token && (
              <button
                className="btn btn-primary"
                onClick={() => navigate("/create-post")}
              >
                Create Post
              </button>
            )}
          </div>
        )}

        <div className="card-grid">
          {posts.map((post) => (
            <div
              key={post.id}
              className="card card-clickable"
              onClick={() => navigate(`/post/${post.id}`)}
            >
              <h3 className="post-card-title">{post.title}</h3>
              <p className="post-excerpt">{post.content}</p>
              <span className="post-date">
                {new Date(post.created_at).toLocaleDateString("en-AU", {
                  day: "numeric", month: "long", year: "numeric"
                })}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}