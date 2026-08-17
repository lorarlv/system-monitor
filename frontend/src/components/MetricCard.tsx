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
  status?: MetricStatus;
  visual?: "bar" | "thermometer";
};

function MetricCard({
  title,
  value,
  percent,
  status,
  visual,
}: MetricCardProps) {
  return (
    <div className="metric-card">
      <h2 className="metric-title">{title}</h2>

      {visual !== "thermometer" && (
        <p className="metric-value">{value}</p>
      )}

      {visual === "bar" && percent !== undefined && status && (
        <>
          <div className="usage-bar">
            <div
              className={`usage-bar-fill ${status}`}
              style={{ width: `${Math.min(percent, 100)}%` }}
            />
          </div>

          <p className={`metric-status ${status}`}>
            {status === "healthy" && "Healthy"}
            {status === "warning" && "Warning"}
            {status === "critical" && "Critical"}
          </p>
        </>
      )}

      {visual === "thermometer" &&
        percent !== undefined &&
        status && (
          <div className="temperature-layout">
            <div className="temperature-info">
              <p className="metric-value">{value}</p>

              <p className={`metric-status ${status}`}>
                {status === "cool" && "Cool"}
                {status === "warm" && "Warm"}
                {status === "hot" && "Hot"}
              </p>
            </div>

            <div className="thermometer">
              <div className="thermometer-tube">
                <div
                  className={`thermometer-mercury ${status}`}
                  style={{ height: `${Math.min(percent, 100)}%` }}
                />
              </div>

              <div className={`thermometer-bulb ${status}`} />
            </div>
          </div>
        )}
    </div>
  );
}

export default MetricCard;