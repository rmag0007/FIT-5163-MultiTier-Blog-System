import { useState } from "react";
import BlogPost from "./BlogPost";

const MOCK_POSTS = [
  {
    id: 1,
    title: "Getting Started with Python",
    content: "Python is a versatile language used in web development, data science, and more. In this post we explore the basics of Python and why it's so popular among beginners and experts alike.",
    author: "Alice"
  },
  {
    id: 2,
    title: "Why Security Matters in Web Apps",
    content: "Security is often an afterthought in web development. This post covers the most common vulnerabilities like SQL injection, XSS, and how to protect against them effectively.",
    author: "Bob"
  },
  {
    id: 3,
    title: "Understanding REST APIs",
    content: "REST APIs are the backbone of modern web applications. Learn how they work, how to design them well, and how to consume them from your frontend applications.",
    author: "Alice"
  }
];

export default function BlogHome() {
  const [selectedPost, setSelectedPost] = useState(null);

  return (
    <div>
      <nav>
        <h1>The Dev Blog</h1>
        <a href="/login">Blogger Login</a>
      </nav>

      {selectedPost ? (
        <>
          <button onClick={() => setSelectedPost(null)}>← Back</button>
          <BlogPost post={selectedPost} />
        </>
      ) : (
        <div>
          <h2>Latest Posts</h2>
          {MOCK_POSTS.map((post) => (
            <div key={post.id} onClick={() => setSelectedPost(post)} style={{ cursor: "pointer", marginBottom: "1rem" }}>
              <h3>{post.title}</h3>
              <p>By {post.author}</p>
              <p>{post.content.substring(0, 100)}...</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}