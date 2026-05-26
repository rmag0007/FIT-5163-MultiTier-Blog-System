import { useState } from "react";
import { useNavigate } from "react-router-dom";
import client from "../api/client";

export default function CreatePost() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleCreate = async () => {
    setError("");
    if (!title || !content) {
      setError("Title and content are required");
      return;
    }
    setLoading(true);
    try {
      await client.post("/posts", { title, content });
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.error || "Failed to create post");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <nav className="navbar">
        <div className="navbar-inner">
          <a href="/" className="navbar-brand">Dev<span>Blog</span></a>
          <div className="navbar-actions">
            <button
              className="btn btn-ghost btn-sm"
              onClick={() => navigate("/dashboard")}
            >
              ← Back
            </button>
          </div>
        </div>
      </nav>

      <div className="container">
        <div style={{ maxWidth: "640px", margin: "3rem auto" }}>
          <h2 style={{ marginBottom: "0.25rem" }}>Create New Post</h2>
          <p style={{ marginBottom: "2rem" }}>
            Write something worth reading.
          </p>

          {error && <div className="alert alert-error">{error}</div>}

          <div className="form-group">
            <label className="form-label">Title</label>
            <input
              className="form-input"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Give your post a title"
              maxLength={200}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Content</label>
            <textarea
              className="form-textarea"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Write your post content here..."
              rows={12}
              style={{ minHeight: "280px" }}
            />
          </div>

          <div style={{ display: "flex", gap: "0.75rem" }}>
            <button
              className="btn btn-primary"
              onClick={handleCreate}
              disabled={loading}
            >
              {loading ? "Publishing..." : "Publish Post"}
            </button>
            <button
              className="btn btn-secondary"
              onClick={() => navigate("/dashboard")}
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}