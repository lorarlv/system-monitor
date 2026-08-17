type MetricCardProps = {
    title: string;
    value: string;
    percent?: number;
    status?: "healthy" | "warning" | "critical";
};

function MetricCard({ title, value, percent, status = "healthy" }: MetricCardProps) {
    return (
        <div className="metric-card">
            <h2 className="metric-title">{title}</h2>
            <p className="metric-value">{value}</p>

            {percent !== undefined && (
                <div className="usage-bar">
                    <div
                        className={`usage-bar-fill ${status}`}
                        style={{ width: `${Math.min(percent, 100)}%` }}
                    />
                </div>
            )}

            {percent !== undefined && (
                <p className={`metric-status ${status}`}>
                    {status === "healthy" && "Healthy"}
                    {status === "warning" && "Warning"}
                    {status === "critical" && "Critical"}
                </p>
            )}
        </div>
    );
}

export default MetricCard;