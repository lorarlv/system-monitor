import Thermometer from "./Thermometer";

type Status = "healthy" | "warning" | "critical";
type TemperatureStatus = "cool" | "warm" | "hot";

type GpuCardProps = {
  usage?: number | null;
  memoryUsed?: number | null;
  memoryTotal?: number | null;
  temperature?: number | null;
};

function getStatus(
  value: number,
  warning: number,
  critical: number
): Status {
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
): TemperatureStatus {
  if (temperature >= 90) {
    return "hot";
  }

  if (temperature >= 70) {
    return "warm";
  }

  return "cool";
}

function GpuCard({
  usage,
  memoryUsed,
  memoryTotal,
  temperature,
}: GpuCardProps) {
  const memoryPercent =
    memoryUsed != null &&
    memoryTotal != null &&
    memoryTotal > 0
      ? (memoryUsed / memoryTotal) * 100
      : null;

  const usageStatus =
    usage == null
      ? undefined
      : getStatus(usage, 50, 80);

  const memoryStatus =
    memoryPercent == null
      ? undefined
      : getStatus(memoryPercent, 70, 90);

  const temperatureStatus =
    temperature == null
      ? undefined
      : getTemperatureStatus(temperature);

  return (
    <div className="metric-card gpu-card">
      <h2 className="metric-title">GPU</h2>

      <div className="gpu-layout">
        <div className="gpu-stats">
          <div className="gpu-section">
            <div className="gpu-metric">
              <span>Usage</span>

              <strong>
                {usage == null
                  ? "Unavailable"
                  : `${usage.toFixed(1)}%`}
              </strong>
            </div>

            {usage != null && usageStatus && (
              <div className="usage-bar">
                <div
                  className={`usage-bar-fill ${usageStatus}`}
                  style={{
                    width: `${Math.min(usage, 100)}%`,
                  }}
                />
              </div>
            )}
          </div>

          <div className="gpu-section">
            <div className="gpu-metric">
              <span>VRAM</span>

              <strong>
                {memoryUsed != null && memoryTotal != null
                  ? `${memoryUsed.toFixed(0)} / ${memoryTotal.toFixed(0)} MB`
                  : "Unavailable"}
              </strong>
            </div>

            {memoryPercent != null && memoryStatus && (
              <div className="usage-bar">
                <div
                  className={`usage-bar-fill ${memoryStatus}`}
                  style={{
                    width: `${Math.min(memoryPercent, 100)}%`,
                  }}
                />
              </div>
            )}
          </div>
        </div>

        <div className="gpu-temperature-section">
          <div className="gpu-temperature-info">
            <span>Temperature</span>

            <strong>
              {temperature == null
                ? "Unavailable"
                : `${temperature.toFixed(1)}°C`}
            </strong>

            {temperatureStatus && (
              <span className={`metric-status ${temperatureStatus}`}>
                {temperatureStatus === "cool" && "Cool"}
                {temperatureStatus === "warm" && "Warm"}
                {temperatureStatus === "hot" && "Hot"}
              </span>
            )}
          </div>

          <Thermometer
            temperature={temperature}
            status={temperatureStatus}
          />
        </div>
      </div>
    </div>
  );
}

export default GpuCard;