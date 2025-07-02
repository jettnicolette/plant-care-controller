# Raspberry Pi Automated Plant Care System 🌱

This project is a working prototype of an automated plant watering system built with a Raspberry Pi 4B, Python, relay control, and soil moisture sensors. The system reads real-time soil moisture levels and triggers a water pump based on custom thresholds.

---

## 💡 Features

- Real-time soil moisture monitoring using capacitive sensors
- Automated water pump control via relay module
- Manual relay testing and sensor diagnostics
- Remote SSH access for full system management
- Expandable for future features like:
  - Runoff pH testing
  - Feeding adjustments based on plant stage
  - Mobile or web-based interface
  - AI-driven growth recommendations

---

## 🛠 Hardware Used

- Raspberry Pi 4B
- MCP3008 Analog-to-Digital Converter
- Capacitive soil moisture sensors
- 5V and 12V water pumps
- Relay modules (5V control side, 12V switching side)
- Breadboard, jumper wires
- External 12V power supply for high-power pump

---

## 📁 Project Structure
├── test_moisture.py # Moisture sensor reading tests
├── test_relay.py # Manual relay control test
├── auto_water.py # Full automation script
├── README.md # This file
├── pinout.md # Hardware pin reference
├── .gitignore # Clean repo setup
├── LICENSE # MIT License

---

## 🔌 Wiring Overview

**MCP3008:**
- CLK → GPIO11 (Pin 23)
- DOUT → GPIO9 (Pin 21)
- DIN → GPIO10 (Pin 19)
- CS → GPIO8 (Pin 24)
- VDD & VREF → 3.3V
- AGND & DGND → GND

**Relay:**
- DC+ → Pi 5V
- DC- → Pi GND
- IN → GPIO17 (Pin 11)
- COM → Pump Power +
- NO → Pump +
- Pump - → Power Supply -

**Moisture Sensor:**
- A0 → MCP3008 CH0
- VCC → 3.3V
- GND → GND

---

## 🚀 Getting Started

1. **SSH into your Pi:**

2. **Run moisture test: python3 test_moisture.py**
   
3. **Control the relay manually: python3 test_relay.py**

4. **Full automation (Coming Soon): python3 auto_water.py**


---

## ⚡ Future Improvements

- Runoff pH detection
- Nutrient dosing automation
- Integrated web dashboard (Next.js + Tailwind)
- AI-driven plant health monitoring
- 3D-printed housing for all components

---

## 📄 License

This project is licensed under the MIT License — see `LICENSE` file for details.

---

## 🤝 Contributing

Solo project for now — expanding to open contributions once stabilized.

---









