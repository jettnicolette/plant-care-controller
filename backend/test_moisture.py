
import spidev
import time

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    result = ((adc[1] & 3) << 8) + adc[2]
    return result

try:
    while True:
        raw_value = read_channel(0) #MCP Channel 0 
        moisture = 1023 - raw_value #invert for ease of reading
        print(f"Moisture Reading: {moisture}")
        time.sleep(1)

except KeyboardInterrupt:
    spi.close()
    print("\nExiting test.")
