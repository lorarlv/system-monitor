export type Metrics = {
    timestamp: string;
    cpu_percent: number;
    cpu_temperature: number | null;
    memory_percent: number;
    disk_percent: number;
    download_rate: number;
    upload_rate: number;
}