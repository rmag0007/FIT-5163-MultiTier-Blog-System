import { useState } from "react";
import { useNavigate } from "react-router-dom";
import client from "../api/client";

export default function Register() {
  const [form, setForm] = useState({
    username: "", email: "", password: "", tier: "basic"
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleRegister = async () => {
    setError("");
    setLoading(true);
    try {
      await client.post("/auth/register", form);
      navigate("/login");
    } catch (err) {
      setError(err.response?.data?.error || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-page">
      <div className="form-card">
        <h2 className="form-title">Create account</h2>
        <p className="form-subtitle">Start tracking your blog analytics</p>

        {error && <div className="alert alert-error">{error}</div>}

        <div className="form-group">
          <label className="form-label">Username</label>
          <input
            className="form-input"
            name="username"
            value={form.username}
            onChange={handleChange}
            placeholder="Choose a username"
          />
        </div>

        <div className="form-group">
          <label className="form-label">Email</label>
          <input
            className="form-input"
            name="email"
            type="email"
            value={form.email}
            onChange={handleChange}
            placeholder="your@email.com"
          />
        </div>

        <div className="form-group">
          <label className="form-label">Password</label>
          <input
            className="form-input"
            name="password"
            type="password"
            value={form.password}
            onChange={handleChange}
            placeholder="Minimum 8 characters"
          />
        </div>

        <div className="form-group">
          <label className="form-label">Account Type</label>
          <select
            className="form-select"
            name="tier"
            value={form.tier}
            onChange={handleChange}
          >
            <option value="basic">Basic — Views and likes only</option>
            <option value="premium">Premium — Full analytics access</option>
          </select>
        </div>

        <button
          className="btn btn-primary form-btn-full"
          onClick={handleRegister}
          disabled={loading}
        >
          {loading ? "Creating account..." : "Create Account"}
        </button>

        <div className="form-footer">
          Already have an account?{" "}
          <a href="/login">Login here</a>
        </div>
      </div>
    </div>
  );
}