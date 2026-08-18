import { memo, useMemo } from "react";

import {
  ResponsiveContainer,
  CartesianGrid,
  Line,
  LineChart,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { Metrics } from "../types/metrics";

type HistoryMetric =
  | "cpu"
  | "memory"
  | "disk"
  | "temperature";

type HistoryChartProps = {
  data: Metrics[];
  metric: HistoryMetric;
};

function getTemperatureColor(temp: number | null): string {
    if (temp === null) return "#4ade80";
    if (temp >= 90) return "#ef4444";
    if (temp >= 70) return "#f59e0b";

    return "#4ade80";
  }

function HistoryChart({data, metric }: HistoryChartProps) {
    const latestTemperature =
        [...data]
        .reverse()
        .find((item) => item.cpu_temperature !== null)
        ?.cpu_temperature ?? null;
    const metricConfig = {
        cpu: {
            label: "CPU Usage",
            unit: "%",
            color: "#4ade80",
            getValue: (item: Metrics) => item.cpu_percent,
            domain: [0, 100],
        },
        memory: {
            label: "RAM Usage",
            unit: "%",
            color: "#4ade80",
            getValue: (item: Metrics) => item.memory_percent,
            domain: [0, 100],
        },
        disk: {
            label: "Disk Usage",
            unit: "%",
            color: "#4ade80",
            getValue: (item: Metrics) => item.disk_percent,
            domain: [0, 100],
        },
        temperature: {
            label: "CPU Temperature",
            unit: "°C",
            color: getTemperatureColor(latestTemperature),
            getValue: (item: Metrics) => item.cpu_temperature,
            domain: [0, 100],
            },
};

    const config = metricConfig[metric];

    const chartData = useMemo(() => {
        return data
            .map((item) => ({
                time: new Date(item.timestamp).toLocaleTimeString(),
                value:
                    metric === "cpu"
                        ? item.cpu_percent
                        : metric === "memory"
                            ? item.memory_percent
                            : metric === "disk"
                                ? item.disk_percent
                                : item.cpu_temperature,
            }))
            .filter((item) => item.value !== null);
    }, [data, metric]);

    return (
        <ResponsiveContainer width="100%" height={250}>
            <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis dataKey="time" />

                <YAxis domain={config.domain} />

                <Tooltip
                    formatter={(value) => [
                    `${Number(value).toFixed(1)}${config.unit}`,
                    config.label,
                ]}
                    contentStyle={{
                    backgroundColor: "#171a21",
                    border: "1px solid #2f3542",
                    borderRadius: "10px",
                }}
                    labelStyle={{
                    color: "#f5f7fa",
                    fontWeight: 600,
                }}
                    itemStyle={{
                    color: config.color,
                }}
                />

            <Line
                type="monotone"
                dataKey="value"
                name={config.label}
                stroke={config.color}
                dot={false}
            />
            </LineChart>
        </ResponsiveContainer>
    );
}

export default memo(HistoryChart);