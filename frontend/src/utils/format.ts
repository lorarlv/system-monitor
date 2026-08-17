export function formatNetworkRate(rate: number): string {
    if (rate >= 1024 ** 3) {
      return `${(rate / 1024 ** 3).toFixed(2)} GB/s`;
    }

    if (rate >= 1024 ** 2) {
      return `${(rate / 1024 ** 2).toFixed(2)} MB/s`;
    }

    if (rate >= 1024) {
      return `${(rate / 1024).toFixed(2)} KB/s`;
    }

    return `${rate.toFixed(0)} B/s`;
  }

export const NETWORK_SCALE_MAX_MBPS = 50;

export function networkPercent(rateBytesPerSecond: number): number {
    const rateMbps = (rateBytesPerSecond * 8) / 1_000_000;

    return Math.min(
        (rateMbps / NETWORK_SCALE_MAX_MBPS) * 100,
        100
    );
}