import { useState, useEffect } from "react";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { fetchStats } from "../services/api";

ChartJS.register(ArcElement, Tooltip, Legend);

function StatsChart() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadStats = async () => {
      try {
        const data = await fetchStats();
        setStats(data);
      } catch (err) {
        console.error("Failed to fetch stats:", err);
      } finally {
        setLoading(false);
      }
    };
    loadStats();
    const interval = setInterval(loadStats, 10000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return <div style={{ color: "#94a3b8", textAlign: "center", padding: "20px" }}>Loading stats...</div>;

  const data = {
    labels: ["High Severity", "Medium Severity", "Low Severity"],
    datasets: [
      {
        label: "Alert Distribution",
        data: stats ? [
          stats.severity_breakdown.HIGH,
          stats.severity_breakdown.MEDIUM,
          stats.severity_breakdown.LOW
        ] : [0, 0, 0],
        backgroundColor: ["#ef4444", "#f59e0b", "#22c55e"],
        borderColor: "rgba(15, 23, 42, 0.8)",
        borderWidth: 2,
      },
    ],
  };

  const options = {
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#cbd5e1',
          padding: 20,
          font: { size: 12 }
        }
      },
      tooltip: {
        backgroundColor: '#1e293b',
        titleColor: '#f8fafc',
        bodyColor: '#f8fafc',
        padding: 10,
        cornerRadius: 8,
      }
    },
    maintainAspectRatio: false,
  };

  return (
    <div style={{ height: "100%", display: "flex", flexDirection: "column" }}>
      <h2 style={{ marginBottom: "20px", fontSize: "20px" }}>📊 Severity Analysis</h2>

      <div style={{ flex: 1, position: "relative", minHeight: "250px" }}>
        <Pie data={data} options={options} />
      </div>

      <div style={{ marginTop: "20px", display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px" }}>
        <div style={{ backgroundColor: "#1e293b", padding: "10px", borderRadius: "8px", textAlign: "center" }}>
          <div style={{ fontSize: "12px", color: "#94a3b8" }}>Total Traffic</div>
          <div style={{ fontSize: "20px", fontWeight: "bold" }}>{stats?.total_traffic || 0}</div>
        </div>
        <div style={{ backgroundColor: "#1e293b", padding: "10px", borderRadius: "8px", textAlign: "center" }}>
          <div style={{ fontSize: "12px", color: "#ef4444" }}>Total Alerts</div>
          <div style={{ fontSize: "20px", fontWeight: "bold", color: "#ef4444" }}>{stats?.total_alerts || 0}</div>
        </div>
      </div>
    </div>
  );
}

export default StatsChart;