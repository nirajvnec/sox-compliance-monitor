import { useState, useEffect } from "react";
import { fetchWithAuth } from "../api";
import MetricCard from "./MetricCard";
import "./Dashboard.css";

function Dashboard({ onLogout }) {
  const [systemInfo, setSystemInfo] = useState(null);
  const [cpu, setCpu] = useState(null);
  const [memory, setMemory] = useState(null);
  const [disk, setDisk] = useState(null);
  const [compliance, setCompliance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Fetch all data from API
  async function loadAllData() {
    setLoading(true);
    setError("");
    try {
      // Fetch all endpoints at the same time (parallel)
      const [sysData, cpuData, memData, diskData, compData] =
        await Promise.all([
          fetchWithAuth("/api/system-info"),
          fetchWithAuth("/api/cpu"),
          fetchWithAuth("/api/memory"),
          fetchWithAuth("/api/disk"),
          fetchWithAuth("/api/compliance"),
        ]);

      setSystemInfo(sysData);
      setCpu(cpuData);
      setMemory(memData);
      setDisk(diskData);
      setCompliance(compData);
    } catch (err) {
      setError("Failed to load data. " + err.message);
    } finally {
      setLoading(false);
    }
  }

  // Load data when Dashboard first appears
  useEffect(() => {
    loadAllData();
  }, []); // Empty array = run once on mount

  if (loading) {
    return <div className="loading">Loading metrics...</div>;
  }

  if (error) {
    return (
      <div className="error-screen">
        <p>{error}</p>
        <button onClick={loadAllData}>Try Again</button>
      </div>
    );
  }

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <h1>SOX Compliance Monitor</h1>
        <div className="header-actions">
          <button className="btn-refresh" onClick={loadAllData}>
            Refresh
          </button>
          <button className="btn-logout" onClick={onLogout}>
            Logout
          </button>
        </div>
      </header>

      {/* Compliance Status Banner */}
      {compliance && (
        <div
          className={`compliance-banner ${
            compliance.overall === "COMPLIANT" ? "banner-pass" : "banner-fail"
          }`}
        >
          <span className="banner-status">{compliance.overall}</span>
          <span className="banner-score">Score: {compliance.score}</span>
        </div>
      )}

      {/* Metric Cards Grid */}
      <div className="metrics-grid">
        {cpu && (
          <MetricCard
            title="CPU Usage"
            value={`${cpu.cpu_percent}%`}
            details={[`Cores: ${cpu.cpu_cores}`]}
          />
        )}
        {memory && (
          <MetricCard
            title="Memory Usage"
            value={`${memory.memory_percent}%`}
            details={[
              `Total: ${memory.total_gb} GB`,
              `Used: ${memory.used_gb} GB`,
              `Free: ${memory.free_gb} GB`,
            ]}
          />
        )}
        {disk && (
          <MetricCard
            title="Disk Usage"
            value={`${disk.disk_percent}%`}
            details={[
              `Total: ${disk.total_gb} GB`,
              `Used: ${disk.used_gb} GB`,
              `Free: ${disk.free_gb} GB`,
            ]}
          />
        )}
        {systemInfo && (
          <MetricCard
            title="System Info"
            value={systemInfo.hostname}
            details={[
              `Platform: ${systemInfo.platform}`,
              `Python: ${systemInfo.python_version}`,
            ]}
          />
        )}
      </div>

      {/* Compliance Checks Table */}
      {compliance && (
        <div className="compliance-section">
          <h2>Compliance Checks</h2>
          <table className="compliance-table">
            <thead>
              <tr>
                <th>Check</th>
                <th>Value</th>
                <th>Threshold</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {compliance.checks.map((check, i) => (
                <tr key={i}>
                  <td>{check.check}</td>
                  <td>{check.value}</td>
                  <td>{check.threshold}</td>
                  <td
                    className={
                      check.status === "PASS" ? "status-pass" : "status-fail"
                    }
                  >
                    {check.status}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
