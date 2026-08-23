using System.Text.Json;
using LibreHardwareMonitor.Hardware;

var computer = new Computer
{
    IsCpuEnabled = true,
    IsGpuEnabled = true,
    IsMemoryEnabled = false,
    IsMotherboardEnabled = false,
    IsControllerEnabled = false,
    IsNetworkEnabled = false,
    IsStorageEnabled = false
};

computer.Open();

List<object> ReadSensors()
{
    var sensors = new List<object>();

    foreach (var hardware in computer.Hardware)
    {
        hardware.Update();

        foreach (var sensor in hardware.Sensors)
        {
            if (sensor.Value is null)
            {
                continue;
            }

            sensors.Add(new
            {
                hardware = hardware.Name,
                hardwareType = hardware.HardwareType.ToString(),
                name = sensor.Name,
                type = sensor.SensorType.ToString(),
                value = sensor.Value
            });
        }

        foreach (var subHardware in hardware.SubHardware)
        {
            subHardware.Update();

            foreach (var sensor in subHardware.Sensors)
            {
                if (sensor.Value is null)
                {
                    continue;
                }

                sensors.Add(new
                {
                    hardware = subHardware.Name,
                    hardwareType = subHardware.HardwareType.ToString(),
                    name = sensor.Name,
                    type = sensor.SensorType.ToString(),
                    value = sensor.Value
                });
            }
        }
    }

    return sensors;
}

try
{
    string? line;

    while ((line = Console.ReadLine()) is not null)
    {
        if (line == "quit")
        {
            break;
        }

        if (line != "read")
        {
            continue;
        }

        var sensors = ReadSensors();

        Console.WriteLine(
            JsonSerializer.Serialize(sensors)
        );

        Console.Out.Flush();
    }
}
finally
{
    computer.Close();
}