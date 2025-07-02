import spidev
import time

# ===== SPI & ADC SETUP =====
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1_350_000

VREF = 3.3               # MCP3008 reference voltage
PH1, voltage4_01 = 4.01, 2.85   # measured at pH 4.01 buffer
PH2, voltage9_18 = 9.18, 1.65   # measured at pH 9.18 buffer

# calculate slope & intercept
slope = (PH2 - PH1) / (voltage9_18 - voltage4_01)
intercept = PH1 - slope * voltage4_01

PH_CHANNEL = 1           # ADC channel your pH board is plugged into

def read_channel(ch):
    """Perform raw read from MCP3008 channel 0–7."""
    adc = spi.xfer2([1, (8 + ch) << 4, 0])
    raw = ((adc[1] & 0x03) << 8) | adc[2]
    return raw

def raw_to_voltage(raw):
    """Convert 0–1023 ADC count to volts."""
    return (raw / 1023) * VREF

def read_ph(channel, samples=30, discard=5):
    """Take multiple readings, trim outliers, average, then convert to pH."""
    volts = []
    for _ in range(samples):
        raw = read_channel(channel)
        volts.append(raw_to_voltage(raw))
        time.sleep(0.02)  # 20 ms between readings
    volts.sort()
    trimmed = volts[discard : -discard]  # throw away highest/lowest
    avg_v = sum(trimmed) / len(trimmed)
    return slope * avg_v + intercept

if __name__ == '__main__':
    try:
        print("Starting pH monitor (CTRL-C to stop)\n")
        while True:
            ph_val = read_ph(PH_CHANNEL)
            print(f"pH = {ph_val:.2f}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nStopping pH sensor test…")
    finally:
        spi.close()
