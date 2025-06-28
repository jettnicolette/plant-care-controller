import time
import RPi.GPIO as GPIO
import spidev

# ====== CONFIGURATION ======
RELAY_PIN = 17  # GPIO pin connected to relay
SECONDS_PER_LITER = 16.38  # Time to dispense 1 liter of water
LITERS_PER_GALLON = 3.78541
SECONDS_PER_GALLON = SECONDS_PER_LITER * LITERS_PER_GALLON
MAX_MOISTURE_READING = 1023  # Maximum raw reading from moisture sensor

# ====== SETUP ======
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000  # SPI speed for MCP3008

# ====== FUNCTIONS ======

def read_channel(channel):
    """Read analog value from MCP3008 channel."""
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    result = ((adc[1] & 3) << 8) + adc[2]
    return result

def get_average_moisture(samples=5, delay=1):
    """Take multiple moisture readings and return average."""
    readings = []
    for _ in range(samples):
        reading = read_channel(0)
        readings.append(reading)
        time.sleep(delay)
    return sum(readings) / len(readings)

def moisture_to_percent(reading):
    """Convert raw moisture reading to percentage (higher = wetter)."""
    percentage = ((MAX_MOISTURE_READING - reading) / MAX_MOISTURE_READING) * 100
    return round(percentage, 1)

def water_for_seconds(seconds):
    """Turn pump on for specified duration."""
    print(f"Watering for {seconds:.2f} seconds...")
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    time.sleep(seconds)
    GPIO.output(RELAY_PIN, GPIO.LOW)
    print("Done watering.")

def water_by_liters(liters):
    """Dispense water based on liters."""
    seconds = liters * SECONDS_PER_LITER
    water_for_seconds(seconds)

def water_by_gallons(gallons):
    """Dispense water based on gallons."""
    seconds = gallons * SECONDS_PER_GALLON
    water_for_seconds(seconds)

# ====== Moisture-Based Sub-Menu ======

def moisture_menu():
    """Sub-menu for moisture monitoring and automated watering."""
    try:
        while True:
            print("\n=== Moisture-Based Watering Menu ===")
            print("1 - Check Moisture Reading")
            print("2 - Water Automatically if Below Threshold")
            print("3 - Water Until Target Moisture is Reached")
            print("4 - Back to Main Menu")

            choice = input("Select an option: ")

            if choice == "1":
                moisture = get_average_moisture()
                print(f"Average Moisture Reading: {moisture:.2f} ({moisture_to_percent(moisture)}%)")

            elif choice == "2":
                threshold = float(input("Set moisture threshold (0-100%): "))
                print("Monitoring moisture... (Ctrl+C to stop)")
                while True:
                    moisture = get_average_moisture()
                    percent = moisture_to_percent(moisture)
                    print(f"Moisture: {moisture:.2f} ({percent}%)")
                    if percent < threshold:
                        print("Below threshold! Watering...")
                        water_by_liters(1)
                        time.sleep(60)
                    else:
                        print("Moisture level OK.")
                    time.sleep(10)

            elif choice == "3":
                target_percent = float(input("Enter target moisture percentage (0-100%): "))
                print("Watering in increments until target moisture is reached...")
                while True:
                    moisture = get_average_moisture()
                    percent = moisture_to_percent(moisture)
                    print(f"Current Moisture: {moisture:.2f} ({percent}%)")
                    if percent >= target_percent:
                        print("Target moisture reached!")
                        break
                    else:
                        print("Watering 0.25 liters...")
                        water_by_liters(0.25)
                        time.sleep(10)

            elif choice == "4":
                break

            else:
                print("Invalid option. Try again.")

    except KeyboardInterrupt:
        print("\nReturning to main menu...")

# ====== MAIN MENU ======

def main_menu():
    """Main menu for manual watering and moisture options."""
    try:
        while True:
            print("\n=== Watering System Menu ===")
            print("1 - Water by Liters")
            print("2 - Water by Gallons")
            print("3 - Custom Time (seconds)")
            print("4 - Moisture-Based Watering Menu")
            print("5 - Exit")

            choice = input("Select an option: ")

            if choice == "1":
                liters = float(input("Enter amount in liters: "))
                water_by_liters(liters)

            elif choice == "2":
                gallons = float(input("Enter amount in gallons: "))
                water_by_gallons(gallons)

            elif choice == "3":
                seconds = float(input("Pump run time in seconds: "))
                water_for_seconds(seconds)

            elif choice == "4":
                moisture_menu()

            elif choice == "5":
                print("Exiting...")
                break

            else:
                print("Invalid option. Try again.")

    except KeyboardInterrupt:
        print("\nProgram stopped manually.")

    finally:
        GPIO.cleanup()
        spi.close()

# ====== PROGRAM ENTRY ======

if __name__ == "__main__":
    main_menu()
