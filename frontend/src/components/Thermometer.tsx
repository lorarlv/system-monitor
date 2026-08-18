type TemperatureStatus = "cool" | "warm" | "hot";

type ThermometerProps = {
  temperature: number | null | undefined;
  status?: TemperatureStatus;
};

function Thermometer({
  temperature,
  status,
}: ThermometerProps) {
  const percent =
    temperature == null
      ? 0
      : Math.max(
          0,
          Math.min(((temperature - 30) / (100 - 30)) * 100, 100)
        );

  return (
    <div className="thermometer">
      <div className="thermometer-tube">
        {status && (
          <div
            className={`thermometer-mercury ${status}`}
            style={{ height: `${percent}%` }}
          />
        )}
      </div>

      <div
        className={
          status
            ? `thermometer-bulb ${status}`
            : "thermometer-bulb unavailable"
        }
      />
    </div>
  );
}

export default Thermometer;