import { useState } from "react";
import { useNavigate } from "react-router-dom";
import client from "../api/client";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async () => {
    setError("");
    setLoading(true);
    try {
      const res = await client.post("/auth/login", { username, password });
      localStorage.setItem("token", res.data.token);
      localStorage.setItem("tier", res.data.tier);
      localStorage.setItem("username", res.data.username);
      localStorage.setItem("user_id", res.data.user_id);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.error || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-page">
      <div className="form-card">
        <h2 className="form-title">Welcome back</h2>
        <p className="form-subtitle">Login to access your dashboard</p>

        {error && <div className="alert alert-error">{error}</div>}

        <div className="form-group">
          <label className="form-label">Username</label>
          <input
            className="form-input"
            placeholder="Your username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label className="form-label">Password</label>
          <input
            className="form-input"
            placeholder="Your password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <button
          className="btn btn-primary form-btn-full"
          onClick={handleLogin}
          disabled={loading}
        >
          {loading ? "Logging in..." : "Login"}
        </button>

        <div className="form-footer">
          Don't have an account?{" "}
          <a href="/register">Register here</a>
          <br />
          <a href="/">← Back to Blog</a>
        </div>
      </div>
    </div>
  );
}