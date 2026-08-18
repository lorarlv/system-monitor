import { useEffect, useState } from "react";

import "./App.css";

import MetricCard from "./components/MetricCard";
import type { Metrics } from "./types/metrics";
import { formatNetworkRate } from "./utils/format";
import HistoryChart from "./components/HistoryChart";
import AlertsPanel from "./components/AlertsPanel";
import type { Alerts } from "./types/alerts";

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

function temperaturePercent(temp: number): number {
  const min = 30;
  const max = 100;

  return Math.max(
    0,
    Math.min(((temp - min) / (max - min)) * 100, 100)
  );
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
  const [alerts, setAlerts] = useState<Alerts | null>(null);

  useEffect(() => {
    const fetchMetrics = () => {
      fetch("http://127.0.0.1:8000/metrics/current")
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

      fetch("http://127.0.0.1:8000/alerts")
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
  const fetchHistory = () => {
    fetch(
      `http://127.0.0.1:8000/metrics/history?minutes=${historyMinutes}`
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
              percent={
                metrics.cpu_temperature === null
                  ? undefined
                  : temperaturePercent(metrics.cpu_temperature)
              }
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
          </div>
          
          {alerts && (
            <AlertsPanel alerts={alerts} />
          )}

          <div className="history-section">
            <div className="history-header">
              <h2>CPU usage history</h2>

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

            {history.length > 0 ? (
              <HistoryChart data={history} />
            ) : (
              <p className="history-empty">No data in this time range.</p>
            )}
          </div>
        </>
      ) : (
        <p className="loading">Loading...</p>
      )}
    </main>
  );
}

export default App;