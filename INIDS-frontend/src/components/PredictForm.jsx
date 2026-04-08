import { useState } from "react";
import { predictTraffic } from "../services/api";

export default function PredictForm() {
  const [form, setForm] = useState({
    src_port: "",
    dst_port: "",
    protocol: "6", // Default to TCP
    packet_size: "",
    flow_duration: ""
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      const res = await predictTraffic({
        src_port: Number(form.src_port),
        dst_port: Number(form.dst_port),
        protocol: Number(form.protocol),
        packet_size: Number(form.packet_size),
        flow_duration: Number(form.flow_duration)
      });
      setResult(res);
    } catch (err) {
      alert("Prediction failed");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getAttackLabel = (prediction) => {
    // Backend returns 0, 1, or "attack" (for demo)
    const p = String(prediction).toLowerCase();
    if (p === "0" || p === "normal") return "🟢 Normal Traffic";
    if (p === "1" || p === "attack") return "🔴 Attack Detected";
    return "❓ Unknown";
  };

  const severityColor = (severity) => {
    if (severity === "LOW") return "#22c55e";
    if (severity === "MEDIUM") return "#f59e0b";
    if (severity === "HIGH") return "#ef4444";
    return "#94a3b8";
  };

  const inputStyle = {
    width: "100%",
    padding: "12px",
    marginBottom: "15px",
    backgroundColor: "#1e293b",
    border: "1px solid #334155",
    borderRadius: "8px",
    color: "white",
    fontSize: "14px",
    outline: "none",
    transition: "border-color 0.3s",
  };

  const buttonStyle = {
    width: "100%",
    padding: "12px",
    backgroundColor: loading ? "#475569" : "#3b82f6",
    color: "white",
    border: "none",
    borderRadius: "8px",
    cursor: loading ? "not-allowed" : "pointer",
    fontSize: "16px",
    fontWeight: "bold",
    transition: "background-color 0.3s",
  };

  return (
    <div style={{ color: "white" }}>
      <h2 style={{ marginBottom: "20px", display: "flex", alignItems: "center", gap: "10px" }}>
        🔍 Traffic Input
      </h2>

      <div style={{ marginBottom: "15px" }}>
        <label style={{ fontSize: "12px", color: "#94a3b8", marginBottom: "5px", display: "block" }}>Source Port</label>
        <input name="src_port" style={inputStyle} placeholder="e.g. 443" onChange={handleChange} value={form.src_port} />
      </div>

      <div style={{ marginBottom: "15px" }}>
        <label style={{ fontSize: "12px", color: "#94a3b8", marginBottom: "5px", display: "block" }}>Destination Port</label>
        <input name="dst_port" style={inputStyle} placeholder="e.g. 80" onChange={handleChange} value={form.dst_port} />
      </div>

      <div style={{ marginBottom: "15px" }}>
        <label style={{ fontSize: "12px", color: "#94a3b8", marginBottom: "5px", display: "block" }}>Protocol (TCP=6, UDP=17)</label>
        <select name="protocol" style={inputStyle} onChange={handleChange} value={form.protocol}>
          <option value="6">TCP (6)</option>
          <option value="17">UDP (17)</option>
          <option value="1">ICMP (1)</option>
        </select>
      </div>

      <div style={{ marginBottom: "15px" }}>
        <label style={{ fontSize: "12px", color: "#94a3b8", marginBottom: "5px", display: "block" }}>Packet Size (Bytes)</label>
        <input name="packet_size" style={inputStyle} placeholder="e.g. 1500" onChange={handleChange} value={form.packet_size} />
      </div>

      <div style={{ marginBottom: "15px" }}>
        <label style={{ fontSize: "12px", color: "#94a3b8", marginBottom: "5px", display: "block" }}>Flow Duration (ms)</label>
        <input name="flow_duration" style={inputStyle} placeholder="e.g. 200" onChange={handleChange} value={form.flow_duration} />
      </div>

      <button onClick={handleSubmit} disabled={loading} style={buttonStyle}>
        {loading ? "Analyzing..." : "Analyze Traffic"}
      </button>

      {result && (
        <div style={{ 
          marginTop: "20px", 
          padding: "15px", 
          backgroundColor: "#0f172a", 
          borderRadius: "10px", 
          border: `1px solid ${severityColor(result.severity)}55` 
        }}>
          <p style={{ margin: "5px 0" }}><b>Result:</b> {getAttackLabel(result.prediction)}</p>
          <p style={{ margin: "5px 0" }}><b>Risk Score:</b> <span style={{ fontWeight: "bold" }}>{result.risk}%</span></p>
          <p style={{ margin: "5px 0" }}><b>Severity:</b> <span style={{ color: severityColor(result.severity), fontWeight: "bold" }}>{result.severity}</span></p> 
        </div>
      )}
    </div>
  );
}
