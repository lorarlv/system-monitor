import Thermometer from "./Thermometer";

type MetricStatus =
  | "healthy"
  | "warning"
  | "critical"
  | "cool"
  | "warm"
  | "hot";

type MetricCardProps = {
  title: string;
  value: string;
  percent?: number;
  temperature?: number;
  status?: MetricStatus;
  visual?: "bar" | "thermometer" | "network";
};

function MetricCard({
  title,
  value,
  percent,
  temperature,
  status,
  visual,
}: MetricCardProps) {
  const temperatureStatus =
    status === "cool" ||
    status === "warm" ||
    status === "hot"
      ? status
      : undefined;

  return (
    <div className="metric-card">
      <h2 className="metric-title">{title}</h2>

      {visual === "thermometer" ? (
        <div className="temperature-layout">
          <div className="temperature-info">
            <p className="metric-value">{value}</p>

            {temperatureStatus && (
              <p className={`metric-status ${temperatureStatus}`}>
                {temperatureStatus === "cool" && "Cool"}
                {temperatureStatus === "warm" && "Warm"}
                {temperatureStatus === "hot" && "Hot"}
              </p>
            )}
          </div>

          {temperature !== undefined && temperatureStatus && (
            <Thermometer
              temperature={temperature}
              status={temperatureStatus}
            />
          )}
        </div>
      ) : (
        <>
          <p className="metric-value">{value}</p>

          {visual === "bar" && percent !== undefined && status && (
            <>
              <div className="usage-bar">
                <div
                  className={`usage-bar-fill ${status}`}
                  style={{
                    width: `${Math.min(percent, 100)}%`,
                  }}
                />
              </div>

              <p className={`metric-status ${status}`}>
                {status === "healthy" && "Healthy"}
                {status === "warning" && "Warning"}
                {status === "critical" && "Critical"}
              </p>
            </>
          )}

          {visual === "network" && percent !== undefined && (
            <div className="network-visual">
              <div className="network-bar">
                <div
                  className="network-bar-fill"
                  style={{
                    width: `${Math.min(percent, 100)}%`,
                  }}
                />
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default MetricCard;