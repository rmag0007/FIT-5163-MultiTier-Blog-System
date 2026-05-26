import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import client from "../api/client";
import BlogPost from "../components/Blog/BlogPost";

export default function BlogPostPage() {
  const { id } = useParams();
  const [post, setPost] = useState(null);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    client.get(`/posts/${id}`)
      .then((res) => setPost(res.data))
      .catch(() => setError("Post not found"));
  }, [id]);

  if (error) return (
    <div className="page">
      <nav className="navbar">
        <div className="navbar-inner">
          <a href="/" className="navbar-brand">Dev<span>Blog</span></a>
        </div>
      </nav>
      <div className="container">
        <div className="empty-state">
          <p>{error}</p>
          <button className="btn btn-primary" onClick={() => navigate("/")}>
            Back to Blog
          </button>
        </div>
      </div>
    </div>
  );

  if (!post) return (
    <div className="page">
      <div className="loading">Loading post...</div>
    </div>
  );

  return (
    <div className="page">
      <nav className="navbar">
        <div className="navbar-inner">
          <a href="/" className="navbar-brand">Dev<span>Blog</span></a>
          <div className="navbar-actions">
            <button
              className="btn btn-ghost btn-sm"
              onClick={() => navigate("/")}
            >
              ← All Posts
            </button>
          </div>
        </div>
      </nav>
      <div className="container">
        <BlogPost post={post} />
      </div>
    </div>
  );
}