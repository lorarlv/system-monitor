import { useEffect, useState } from "react";

import "./App.css";

import AlertsPanel from "./components/AlertsPanel";
import GpuCard from "./components/GpuCard";
import HistoryChart from "./components/HistoryChart";
import MetricCard from "./components/MetricCard";

import type { Alerts } from "./types/alerts";
import type { Metrics } from "./types/metrics";

import { formatNetworkRate } from "./utils/format";

function getStatus(
  value: number,
  warning: number,
  critical: number
): "healthy" | "warning" | "critical" {
  if (value >= critical) {
    return "critical";
  }

  if (value >= warning) {
    return "warning";
  }

  return "healthy";
}

function getTemperatureStatus(
  temperature: number
): "cool" | "warm" | "hot" {
  if (temperature >= 90) {
    return "hot";
  }

  if (temperature >= 70) {
    return "warm";
  }

  return "cool";
}

function adaptiveNetworkPercent (
  currentRate: number,
  maxRate: number
): number {
  if (maxRate <= 0) {
    return 0;
  }

  return Math.min((currentRate / maxRate) * 100, 100);
}

function App() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [maxDownloadRate, setMaxDownloadRate] = useState(1);
  const [maxUploadRate, setMaxUploadRate] = useState(1);

  const [history, setHistory] = useState<Metrics[]>([]);
  const [historyMinutes, setHistoryMinutes] = useState(5);
  const [historyMetric, setHistoryMetric] = useState<
    "cpu" 
    | "memory" 
    | "disk" 
    | "temperature"
    | "gpu"
    | "vram"
  >("cpu");
  
  const [alerts, setAlerts] = useState<Alerts | null>(null);

  const [isShuttingDown, setIsShuttingDown] = useState(false);

  function shutdownMonitor() {
    setIsShuttingDown(true);

    fetch("/shutdown", {
      method: "POST",
    }).catch(() => {
      // Losing connection is expected because server is shutting down.
    });
  }

  useEffect(() => {
    if (isShuttingDown) {
      return;
    }

    const fetchMetrics = () => {
      fetch("/metrics/current")
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
          }
      
          return response.json();
        })
        .then ((data) => {
          setMetrics(data);

          setMaxDownloadRate((currentMax) =>
            Math.max(currentMax, data.download_rate)
          );

          setMaxUploadRate((currentMax) =>
            Math.max(currentMax, data.upload_rate)
          );
        })
        .catch((error) => {
          console.error("Failed to fetch metrics:", error);
        });

      fetch("/alerts")
        .then ((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
          }

          return response.json();
        })

        .then((data) => {
          setAlerts(data);
        })

        .catch((error) => {
          console.error("Failed to fetch alerts:", error);
        });
    };

    fetchMetrics();

    const interval = setInterval(fetchMetrics, 1000);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (isShuttingDown) {
      return;
    }
    
    const fetchHistory = () => {
      fetch(
        `/metrics/history?minutes=${historyMinutes}`
      )
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
          }

          return response.json();
        })
        .then((data) => {
          setHistory(data);
        })
        .catch((error) => {
          console.error("Failed to fetch history:", error);
        });
    };

    fetchHistory();

    const interval = setInterval(fetchHistory, 5000);

    return () => clearInterval(interval);
  }, [historyMinutes]);

  const temperatureStatus =
    metrics?.cpu_temperature != null
      ? getTemperatureStatus(metrics.cpu_temperature)
      : undefined;

  if (isShuttingDown) {
    return (
      <main className="app">
        <div className="shutdown-message">
          <h1>System Monitor stopped</h1>
          <p>You can close this tab.</p>
        </div>
      </main>
    );
  }
  
  return (
    <main className="app">
      <h1 className="app-title">System Monitor</h1>
      
      {metrics ? (
        <>
          <div className="metrics-grid">
            <MetricCard 
              title="CPU"
              value={`${metrics.cpu_percent.toFixed(1)}%`}
              percent={metrics.cpu_percent}
              status={getStatus(metrics.cpu_percent, 50, 80)}
              visual="bar"
            />
            <MetricCard
              title="CPU temperature"
              value={
                metrics.cpu_temperature === null
                  ? "Unavailable"
                  : `${metrics.cpu_temperature.toFixed(1)}°C`
              }
              temperature={metrics.cpu_temperature ?? undefined}
              status={temperatureStatus}
              visual="thermometer"
            />
            <MetricCard 
              title="RAM"
              value={`${metrics.memory_percent.toFixed(1)}%`}
              percent={metrics.memory_percent}
              status={getStatus(metrics.memory_percent, 70, 90)}
              visual="bar"
            />
            <MetricCard 
              title="Disk"
              value={`${metrics.disk_percent.toFixed(1)}%`}
              percent={metrics.disk_percent}
              status={getStatus(metrics.disk_percent, 80, 90)}
              visual="bar"
            />
            <MetricCard 
              title="↓ Download ↓"
              value={formatNetworkRate(metrics.download_rate)}
              percent={adaptiveNetworkPercent(metrics.download_rate, maxDownloadRate)}
              visual="network"
            />
            <MetricCard 
              title="↑ Upload ↑"
              value={formatNetworkRate(metrics.upload_rate)}
              percent={adaptiveNetworkPercent(metrics.upload_rate, maxUploadRate)}
              visual="network"
            />
            <GpuCard
              usage={metrics.gpu_usage}
              memoryUsed={metrics.gpu_memory_used}
              memoryTotal={metrics.gpu_memory_total}
              temperature={metrics.gpu_temperature}
            />
          </div>
          
          {alerts && (
            <AlertsPanel alerts={alerts} />
          )}

          <div className="history-section">
            <div className="history-header">
              <h2>System history</h2>
              <div className="history-controls">
                <label>
                  Metric{" "}
                  <select
                    value={historyMetric}
                    onChange={(event) =>
                      setHistoryMetric(
                        event.target.value as
                          | "cpu"
                          | "temperature"
                          | "memory"
                          | "disk"
                          | "gpu"
                          | "vram"
                      )
                    }
                  >
                    <option value="cpu">CPU usage</option>
                    <option value="temperature">CPU temperature</option>
                    <option value="memory">RAM usage</option>
                    <option value="disk">Disk usage</option>
                    <option value="gpu">GPU usage</option>
                    <option value="vram">VRAM usage</option>
                  </select>
                </label>

                <label>
                  Time Range{" "}
                  <select
                    value={historyMinutes}
                    onChange={(event) =>
                      setHistoryMinutes(Number(event.target.value))
                    }
                  >
                    <option value={1}>1 minute</option>
                    <option value={5}>5 minutes</option>
                    <option value={15}>15 minutes</option>
                    <option value={60}>1 hour</option>
                  </select>
                </label>
              </div>
            </div>

            {history.length > 0 ? (
              <HistoryChart 
                data={history}
                metric={historyMetric} />
            ) : (
              <p className="history-empty">No data in this time range.</p>
            )}
          </div>
        </>
      ) : (
        <p className="loading">Loading...</p>
      )}

      <button
        className="shutdown-button"
        onClick={shutdownMonitor}
      >
        Stop System Monitor
      </button>
    </main>
  );
}

export default App;