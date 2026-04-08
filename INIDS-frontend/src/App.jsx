import PredictForm from "./components/PredictForm";
import AlertsTable from "./components/AlertsTable";
import StatsChart from "./components/StatsChart";

function App() {
  return (
    <div style={{ padding: "40px", maxWidth: "1400px", margin: "auto" }}>
      {/* Header Section */}
      <header style={{
        textAlign: "left",
        marginBottom: "40px",
        borderLeft: "4px solid var(--primary)",
        paddingLeft: "20px"
      }}>
        <h1 style={{ fontSize: "3rem", marginBottom: "8px", fontWeight: "700" }}>
          INIDS <span style={{ color: "var(--primary)" }}>Intelligence</span>
        </h1>
        <p style={{ color: "var(--text-muted)", fontSize: "1.1rem" }}>
          Intelligent Network Intrusion Detection & Real-time Visualization
        </p>
      </header>

      {/* Dashboard Grid */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "350px 1fr",
        gap: "30px",
        alignItems: "start"
      }}>

        {/* Left Side: Input Form */}
        <aside className="glass" style={{
          padding: "30px",
          borderRadius: "20px",
          position: "sticky",
          top: "40px"
        }}>
          <PredictForm />
        </aside>

        {/* Right Side: Visuals & Data */}
        <main style={{ display: "flex", flexDirection: "column", gap: "30px" }}>

          <div style={{
            display: "grid",
            gridTemplateColumns: "1fr 400px",
            gap: "30px"
          }}>
            {/* Stats Summary Panel */}
            <section className="glass" style={{ padding: "30px", borderRadius: "20px" }}>
              <StatsChart />
            </section>

            {/* Integration Panel Placeholder or Extra Info */}
            <section className="glass" style={{
              padding: "30px",
              borderRadius: "20px",
              background: "linear-gradient(135deg, var(--bg-card) 0%, #1e1b4b 100%)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              textAlign: "center"
            }}>
              <div style={{ fontSize: "50px", marginBottom: "20px" }}>🛡️</div>
              <h3 style={{ marginBottom: "10px" }}>System Status: Protected</h3>
              <p style={{ color: "var(--text-muted)", fontSize: "0.9rem" }}>
                AI engine is monitoring all incoming traffic logs. Any suspicious activity will trigger a high-severity alert.
              </p>
            </section>
          </div>

          {/* Alerts Table - Wide Panel */}
          <section className="glass" style={{ padding: "30px", borderRadius: "20px" }}>
            <AlertsTable />
          </section>

        </main>
      </div>
    </div>
  );
}

export default App;