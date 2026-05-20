import { useEffect, useState } from "react";
import client from "../api/client";
import BasicDashboard from "../components/Dashboard/BasicDashboard";
import PremiumDashboard from "../components/Dashboard/PremiumDashboard";

export default function Dashboard() {
  const [stats, setStats] = useState([]);
  const tier = localStorage.getItem("tier");

  useEffect(() => {
    const endpoint = tier === "premium" ? "/dashboard/stats/premium" : "/dashboard/stats/basic";
    client.get(endpoint).then((res) => setStats(res.data));
  }, [tier]);

  return (
    <div>
      <h1>{tier === "premium" ? "Premium" : "Basic"} Dashboard</h1>
      {tier === "premium"
        ? <PremiumDashboard stats={stats} />
        : <BasicDashboard stats={stats} />}
    </div>
  );
}