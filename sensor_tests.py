import spidev
import time

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# Channel definitions
PH_CHANNEL = 1
TDS_CHANNEL = 2

REFERENCE_VOLTAGE = 5.18

def read_channel(channel):
    assert 0 <= channel <= 7, "Invalid channel"
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def convert_voltage(raw_value):
    return (raw_value / 1023) * REFERENCE_VOLTAGE

def convert_ph(voltage):
    return 7 + ((voltage - 2.5) * (7 / 2.5))

def convert_tds(voltage):
    tds_ppm = (133.42 * voltage**3) - (255.86 * voltage**2) + (857.39 * voltage)
    tds_ppm *= 0.5  # Correction factor
    return tds_ppm

def read_ph():
    raw = read_channel(PH_CHANNEL)
    voltage = convert_voltage(raw)
    ph = convert_ph(voltage)
    print(f"Instant pH Reading: {ph:.2f}")

def read_ph_avg():
    readings = []
    for _ in range(60):
        readings.append(read_channel(PH_CHANNEL))
        time.sleep(1)
    avg_raw = sum(readings) / len(readings)
    voltage = convert_voltage(avg_raw)
    ph = convert_ph(voltage)
    print(f"Average pH Reading over 1 minute: {ph:.2f}")

def read_tds():
    raw = read_channel(TDS_CHANNEL)
    voltage = convert_voltage(raw)
    tds_ppm = convert_tds(voltage)
    print(f"Instant TDS Reading: {tds_ppm:.2f} ppm")

def read_tds_avg():
    readings = []
    for _ in range(60):
        readings.append(read_channel(TDS_CHANNEL))
        time.sleep(1)
    avg_raw = sum(readings) / len(readings)
    voltage = convert_voltage(avg_raw)
    tds_ppm = convert_tds(voltage)
    print(f"Average TDS Reading over 1 minute: {tds_ppm:.2f} ppm")

def ph_mode():
    while True:
        print("\n--- pH Mode ---")
        print("1. Instant pH Reading")
        print("2. 60-Second Average pH Reading")
        print("3. Return to Main Menu")
        choice = input("Select an option: ")
        if choice == "1":
            read_ph()
        elif choice == "2":
            read_ph_avg()
        elif choice == "3":
            break
        else:
            print("Invalid selection.")

def tds_mode():
    while True:
        print("\n--- TDS Mode ---")
        print("1. Instant TDS Reading")
        print("2. 60-Second Average TDS Reading")
        print("3. Return to Main Menu")
        choice = input("Select an option: ")
        if choice == "1":
            read_tds()
        elif choice == "2":
            read_tds_avg()
        elif choice == "3":
            break
        else:
            print("Invalid selection.")

def main():
    while True:
        print("\n=== Sensor Testing Menu ===")
        print("1. pH Mode")
        print("2. TDS Mode")
        print("3. Exit")
        choice = input("Select a mode: ")

        if choice == "1":
            ph_mode()
        elif choice == "2":
            tds_mode()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()
