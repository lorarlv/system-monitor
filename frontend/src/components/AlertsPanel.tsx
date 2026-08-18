import type { Alerts } from "../types/alerts";

type AlertsPanelProps = {
    alerts: Alerts;
};

function AlertsPanel({ alerts }: AlertsPanelProps) {
    const hasAlerts =
        alerts.cpu ||
        alerts.temperature ||
        alerts.ram ||
        alerts.disk;

    return (
        <section className="alerts-panel">
            <h2>Active alerts</h2>

            {!hasAlerts && (
                <p className="alerts-clear">
                    No active alerts
                </p>
            )}

            {alerts.cpu && (
                <p className="alert-message">
                    CPU usage has remained critically high
                </p>
            )}

            {alerts.temperature && (
                <p className="alert-message">
                    CPU temperature has remained critically high
                </p>
            )}

            {alerts.ram && (
                <p className="alert-message">
                    RAM usage has remained critically high
                </p>
            )}

            {alerts.disk && (
                <p className="alert-message">
                    Disk usage has remained critically high
                </p>
            )}
        </section>
    );
}

export default AlertsPanel;