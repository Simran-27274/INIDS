import { useState, useEffect } from "react";
import { fetchAlerts } from "../services/api";

export default function AlertsTable() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const loadAlerts = async () => {
      try {
        const data = await fetchAlerts();
        setAlerts(data || []);
      } catch (err) {
        console.error("Failed to fetch alerts:", err);
      }
    };
    loadAlerts();

    const interval = setInterval(loadAlerts, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const severityBadge = (severity) => {
    let color = "var(--text-muted)";
    let bg = "rgba(148, 163, 184, 0.1)";

    if (severity === "HIGH") {
      color = "var(--danger)";
      bg = "rgba(239, 68, 68, 0.1)";
    } else if (severity === "MEDIUM") {
      color = "var(--warning)";
      bg = "rgba(245, 158, 11, 0.1)";
    } else if (severity === "LOW") {
      color = "var(--success)";
      bg = "rgba(34, 197, 94, 0.1)";
    }

    return (
      <span style={{
        color,
        backgroundColor: bg,
        padding: "4px 12px",
        borderRadius: "20px",
        fontSize: "12px",
        fontWeight: "600",
        border: `1px solid ${color}44`
      }}>
        {severity}
      </span>
    );
  };

  return (
    <div>
      <h2 style={{ marginBottom: "20px", fontSize: "20px" }}>🚨 Recent Security Alerts</h2>

      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "separate", borderSpacing: "0 8px" }}>
          <thead>
            <tr>
              <th style={{ textAlign: "left", padding: "12px", color: "var(--text-muted)", fontSize: "12px", textTransform: "uppercase" }}>ID</th>
              <th style={{ textAlign: "left", padding: "12px", color: "var(--text-muted)", fontSize: "12px", textTransform: "uppercase" }}>Type</th>
              <th style={{ textAlign: "left", padding: "12px", color: "var(--text-muted)", fontSize: "12px", textTransform: "uppercase" }}>Risk Score</th>
              <th style={{ textAlign: "left", padding: "12px", color: "var(--text-muted)", fontSize: "12px", textTransform: "uppercase" }}>Severity</th>
            </tr>
          </thead>
          <tbody>
            {alerts.length === 0 ? (
              <tr>
                <td colSpan="4" style={{ textAlign: "center", padding: "40px", color: "var(--text-muted)" }}>
                  Searching for network threats...
                </td>
              </tr>
            ) : (
              alerts.map((a) => (
                <tr key={a.id} style={{ backgroundColor: "rgba(30, 41, 59, 0.5)", borderRadius: "10px" }}>
                  <td style={{ padding: "12px", borderTopLeftRadius: "10px", borderBottomLeftRadius: "10px", color: "var(--primary)", fontWeight: "bold" }}>#{a.traffic_id}</td>
                  <td style={{ padding: "12px" }}>{a.attack_type}</td>
                  <td style={{ padding: "12px" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                      <div style={{ width: "60px", height: "6px", backgroundColor: "#1e293b", borderRadius: "3px", overflow: "hidden" }}>
                        <div style={{ width: `${a.risk_score}%`, height: "100%", backgroundColor: a.risk_score > 70 ? "var(--danger)" : "var(--warning)" }}></div>
                      </div>
                      <span>{a.risk_score}%</span>
                    </div>
                  </td>
                  <td style={{ padding: "12px", borderTopRightRadius: "10px", borderBottomRightRadius: "10px" }}>
                    {severityBadge(a.severity)}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
