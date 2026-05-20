import { useEffect, useRef } from "react";
import { v4 as uuidv4 } from "uuid";
import client from "../../api/client";

// Generate once per browser session
const SESSION_ID = sessionStorage.getItem("session_id") || (() => {
  const id = uuidv4();
  sessionStorage.setItem("session_id", id);
  return id;
})();

export default function BlogPost({ post }) {
  const startTime = useRef(Date.now());

  useEffect(() => {
    // Track page view on mount
    client.post("/track", {
      post_id: post.id,
      session_id: SESSION_ID,
      event_type: "view",
    });

    // Track time spent on unmount
    return () => {
      const seconds = Math.floor((Date.now() - startTime.current) / 1000);
      client.post("/track", {
        post_id: post.id,
        session_id: SESSION_ID,
        event_type: "view",
        time_spent_seconds: seconds,
      });
    };
  }, [post.id]);

  const handleLike = () => {
    client.post("/track", {
      post_id: post.id,
      session_id: SESSION_ID,
      event_type: "like",
    });
  };

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
      <button onClick={handleLike}>👍 Like</button>
    </article>
  );
}