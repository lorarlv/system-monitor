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

type HistoryChartProps = {data: Metrics[]};

function HistoryChart({ data }: HistoryChartProps) {
    const chartData = data.map((metric) => ({
        time: new Date(metric.timestamp).toLocaleTimeString(),
        cpu: metric.cpu_percent,
    }));

    return (
        <ResponsiveContainer width="100%" height={250}>
            <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis domain={[0, 100]} />
                <Tooltip
                    formatter={(value) => [`${Number(value).toFixed(1)}%`, "CPU usage"]}
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
                        color: "#4ade80",
                    }}
                />

                <Line
                    type="monotone"
                    dataKey="cpu"
                    name="CPU usage"
                    stroke="#4ade80"
                    dot={false}
                />
            </LineChart>
        </ResponsiveContainer>
    );
}

export default HistoryChart;