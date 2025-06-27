import spidev
import time
import RPi.GPIO as GPIO

RELAY_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# Read from MCP3008
def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    result = ((adc[1] & 3) << 8) + adc[2]
    return result

# Calculate Moisture
def calculate_average_moisture():
    readings = []
    for _ in range(10):
        raw_value = read_channel(0)
        moisture = 1023 - raw_value
        readings.append(moisture)
        time.sleep(1)
    return sum(readings) / len(readings)

# Watering Function
def water_plant(duration=5):
    print(f"Watering for {duration} seconds...")
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(RELAY_PIN, GPIO.LOW)
    print("Done watering.")

# Main Mode Loop
try:
    while True:
        print("\nSelect a Mode:")
        print("1 - Auto Water if Below Threshold")
        print("2 - Manual Water & Moisture Display")
        print("3 - Exit")
        
        mode = input("Enter mode number: ")

        if mode == "1":
            threshold = float(input("Set moisture threshold (0-1023): "))
            print("Monitoring... Press Ctrl+C to stop.")
            while True:
                avg_moisture = calculate_average_moisture()
                print(f"Average Moisture: {avg_moisture:.1f}")

                if avg_moisture < threshold:
                    print("Below threshold! Watering...")
                    water_plant()
                else:
                    print("Moisture level okay.")

                time.sleep(12 * 60 * 60)  # 12-hour wait

        elif mode == "2":
            custom_time = float(input("Pump run time (seconds): "))
            avg_moisture = calculate_average_moisture()
            print(f"Average Moisture: {avg_moisture:.1f}")
            water_plant(custom_time)

        elif mode == "3":
            print("Exiting...")
            break

        else:
            print("Invalid option. Try again.")

except KeyboardInterrupt:
    print("\nProgram stopped manually.")

finally:
    GPIO.cleanup()
    spi.close()
