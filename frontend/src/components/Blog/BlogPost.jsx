import { useEffect, useRef, useState } from "react";
import { v4 as uuidv4 } from "uuid";
import client from "../../api/client";

const SESSION_ID = sessionStorage.getItem("session_id") || (() => {
  const id = uuidv4();
  sessionStorage.setItem("session_id", id);
  return id;
})();

export default function BlogPost({ post }) {
  const startTime = useRef(Date.now());
  const maxScroll = useRef(0);
  const hasTrackedView = useRef(false); // prevents double firing

  // Persist liked state in localStorage per post
  const likedKey = `liked_post_${post.id}`;
  const [liked, setLiked] = useState(() => {
    return localStorage.getItem(likedKey) === "true";
  });

  const sharedKey = `shared_post_${post.id}`;
  const [shared, setShared] = useState(() => {
    return localStorage.getItem(sharedKey) === "true";
  });

  const [comment, setComment] = useState("");
  const [commentPosted, setCommentPosted] = useState(false);

  // Check if current user is the author — don't track own views
  const currentUserId = localStorage.getItem("user_id");
  const isAuthor = currentUserId && parseInt(currentUserId) === post.author_id;

  useEffect(() => {
    const handleScroll = () => {
      const scrolled = window.scrollY + window.innerHeight;
      const total = document.documentElement.scrollHeight;
      const percent = Math.floor((scrolled / total) * 100);
      if (percent > maxScroll.current) {
        maxScroll.current = Math.min(percent, 100);
      }
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  useEffect(() => {
    // Don't track if author is viewing their own post
    if (isAuthor) return;

    // Don't track if already tracked this session
    if (hasTrackedView.current) return;
    hasTrackedView.current = true;

    // Single view event on mount
    client.post("/track", {
      post_id: post.id,
      session_id: SESSION_ID,
      event_type: "view",
      time_spent_seconds: 0,
      scroll_depth_percent: 0
    }).catch(() => {});

    // Send final time + scroll on unmount
    return () => {
      const seconds = Math.floor((Date.now() - startTime.current) / 1000);
      client.post("/track", {
        post_id: post.id,
        session_id: SESSION_ID,
        event_type: "view",
        time_spent_seconds: seconds,
        scroll_depth_percent: maxScroll.current
      }).catch(() => {});
    };
  }, [post.id, isAuthor]);

  const trackEvent = (event_type) => {
    client.post("/track", {
      post_id: post.id,
      session_id: SESSION_ID,
      event_type,
      time_spent_seconds: Math.floor((Date.now() - startTime.current) / 1000),
      scroll_depth_percent: maxScroll.current
    }).catch(() => {});
  };

  const handleLike = () => {
    if (liked) return;
    trackEvent("like");
    setLiked(true);
    localStorage.setItem(likedKey, "true");
  };

  const handleShare = () => {
    if (shared) return;
    trackEvent("share");
    setShared(true);
    localStorage.setItem(sharedKey, "true");
    navigator.clipboard?.writeText(window.location.href);
    alert("Link copied to clipboard!");
  };

  const handleComment = () => {
    if (!comment.trim()) return;
    trackEvent("comment");
    setComment("");
    setCommentPosted(true);
  };

  return (
    <article>
      <div className="blog-hero">
        <h1>{post.title}</h1>
        <div className="blog-meta">
          <span>
            {new Date(post.created_at).toLocaleDateString("en-AU", {
              day: "numeric", month: "long", year: "numeric"
            })}
          </span>
          {isAuthor && (
            <span style={{ color: "var(--accent)", fontSize: "0.8rem" }}>
              ✍ Your post — views not tracked
            </span>
          )}
        </div>
      </div>

      <p className="blog-content">{post.content}</p>

      <div className="blog-actions">
        <button
          className={`btn ${liked ? "btn-secondary" : "btn-primary"}`}
          onClick={handleLike}
          disabled={liked}
        >
          {liked ? "👍 Liked!" : "👍 Like"}
        </button>
        <button
          className="btn btn-secondary"
          onClick={handleShare}
          disabled={shared}
        >
          {shared ? "🔗 Shared!" : "🔗 Share"}
        </button>
      </div>

      <div className="comment-section">
        <h3>Leave a Comment</h3>
        {commentPosted && (
          <div className="alert alert-success">
            Comment posted — thank you!
          </div>
        )}
        <div className="form-group">
          <textarea
            className="form-textarea"
            placeholder="Write your comment..."
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            rows={4}
          />
        </div>
        <button className="btn btn-primary" onClick={handleComment}>
          Post Comment
        </button>
      </div>
    </article>
  );
}