function PredictionPanel() {
  return (
    <div>
      <h2>🔍 Prediction Panel</h2>

      <input placeholder="Source Bytes" style={inputStyle} />
      <input placeholder="Destination Bytes" style={inputStyle} />
      <input placeholder="Protocol Type" style={inputStyle} />

      <button style={btnStyle}>Analyze Traffic</button>
    </div>
  );
}

const inputStyle = {
  width: "100%",
  padding: "10px",
  margin: "8px 0",
  borderRadius: "6px",
  border: "none"
};

const btnStyle = {
  width: "100%",
  padding: "10px",
  marginTop: "10px",
  background: "#2563eb",
  color: "white",
  border: "none",
  borderRadius: "6px",
  cursor: "pointer"
};

export default PredictionPanel;