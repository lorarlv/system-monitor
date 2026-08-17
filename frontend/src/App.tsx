import { useEffect, useState } from "react";

type Metrics = {
  timestamp: string;
  cpu_percent: number;
  cpu_temperature: number | null;
  memory_percent: number;
  disk_percent: number;
  download_rate: number;
  upload_rate: number;
}

function App() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);

  function formatNetworkRate(rate: number): string {
    if (rate >= 1024 ** 3) {
      return `${(rate / 1024 ** 3).toFixed(2)} GB/s`;
    }

    if (rate >= 1024 ** 2) {
      return `${(rate / 1024 ** 2).toFixed(2)} MB/s`;
    }

    if (rate >= 1024) {
      return `${(rate / 1024).toFixed(2)} KB/s`;
    }

    return `${rate.toFixed(0)} B/s`;
  }

  useEffect(() => {
    const fetchMetrics = () => {
      fetch("http://127.0.0.1:8000/metrics/current")
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
          }
      
          return response.json();
        })
        .then ((data) => {setMetrics(data)})
        .catch((error) => {
          console.error("Failed to fetch metrics:", error);
        });
      };
      
      fetchMetrics();

      const interval = setInterval(fetchMetrics, 1000);

      return () => clearInterval(interval);
  }, []);

  return (
    <>
      <h1>System Monitor</h1>
      
      {metrics ? (
        <div>
          <p>CPU: {metrics.cpu_percent.toFixed(1)}%</p>
            <p>CPU temperature:{" "}{metrics.cpu_temperature === null ? "Unavailable" : `${metrics.cpu_temperature.toFixed(1)}°C`}</p>
          <p>RAM: {metrics.memory_percent.toFixed(1)}%</p>
          <p>Disk: {metrics.disk_percent.toFixed(1)}%</p>
          <p>Download: {formatNetworkRate(metrics.download_rate)}</p>
          <p>Upload: {formatNetworkRate(metrics.upload_rate)}</p>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </>
  );
}

export default App;