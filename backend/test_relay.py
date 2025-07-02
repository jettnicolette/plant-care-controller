
import RPi.GPIO as GPIO
import time

RELAY_PIN = 17  # Update if using a different GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

try:
    while True:
        cmd = input("Type 'on', 'off', or 'exit': ").strip().lower()
        if cmd == "on":
            GPIO.output(RELAY_PIN, GPIO.HIGH)
            print("Relay ON")
        elif cmd == "off":
            GPIO.output(RELAY_PIN, GPIO.LOW)
            print("Relay OFF")
        elif cmd == "exit":
            GPIO.cleanup()
            print("Exiting.")
            break
        else:
            print("Unknown command.")
except KeyboardInterrupt:
    GPIO.cleanup()
