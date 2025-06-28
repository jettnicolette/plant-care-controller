import spidev
import time

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# Channel for pH sensor on MCP3008
PH_CHANNEL = 1

# Reference voltage for conversion (matches MCP3008 VREF when powered at 5V)
REFERENCE_VOLTAGE = 5.0

# Conversion function: raw ADC to voltage
def convert_voltage(raw_value):
    return (raw_value / 1023) * REFERENCE_VOLTAGE

# Conversion function: voltage to pH (linear approximation)
def convert_ph(voltage):
    return 7 + ((voltage - 2.5) * (7 / 2.5))

# Read raw ADC value from specified channel
def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    return ((adc[1] & 3) << 8) + adc[2]

# Main loop: print raw, voltage, and calculated pH every second
if __name__ == "__main__":
    try:
        print("Starting pH continuous read. Press Ctrl+C to stop.")
        while True:
            raw = read_channel(PH_CHANNEL)
            voltage = convert_voltage(raw)
            ph = convert_ph(voltage)
            print(f"Raw ADC: {raw:4d} | Voltage: {voltage:.3f} V | pH: {ph:.2f}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\npH continuous read stopped.")
