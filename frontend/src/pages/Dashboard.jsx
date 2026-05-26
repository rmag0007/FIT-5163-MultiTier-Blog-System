import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import client from "../api/client";
import BasicDashboard from "../components/Dashboard/BasicDashboard";
import PremiumDashboard from "../components/Dashboard/PremiumDashboard";

export default function Dashboard() {
  const [stats, setStats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const tier = localStorage.getItem("tier");
  const username = localStorage.getItem("username");
  const navigate = useNavigate();

  useEffect(() => {
    const endpoint = tier === "premium"
      ? "/dashboard/stats/premium"
      : "/dashboard/stats/basic";
    client.get(endpoint)
      .then((res) => setStats(res.data))
      .catch(() => setError("Failed to load stats"))
      .finally(() => setLoading(false));
  }, [tier]);

  const handleLogout = async () => {
    await client.post("/auth/logout");
    localStorage.removeItem("token");
    localStorage.removeItem("tier");
    localStorage.removeItem("username");
    navigate("/login");
  };

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
              View Blog
            </button>
            <button
              className="btn btn-secondary btn-sm"
              onClick={handleLogout}
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      <div className="container">
        <div className="dashboard-header">
          <div className="dashboard-header-left">
            <h1>Dashboard</h1>
            <p>
              Welcome back, {username} &nbsp;
              <span className={`badge badge-${tier}`}>{tier}</span>
            </p>
          </div>
          <div className="dashboard-actions">
            <button
              className="btn btn-primary"
              onClick={() => navigate("/create-post")}
            >
              + New Post
            </button>
          </div>
        </div>

        {loading && <div className="loading">Loading your analytics...</div>}
        {error && <div className="alert alert-error">{error}</div>}

        {!loading && !error && (
          tier === "premium"
            ? <PremiumDashboard stats={stats} />
            : <BasicDashboard stats={stats} />
        )}

        {tier !== "premium" && !loading && (
          <div className="upgrade-banner">
            <p>
              Upgrade to <strong>Premium</strong> to unlock time series,
              scroll depth, country breakdown and more.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}