# Raspberry Pi Automated Plant Care - Pin Reference

## MCP3008 ADC:
- CLK → GPIO11 (Pin 23)
- DOUT → GPIO9 (Pin 21)
- DIN → GPIO10 (Pin 19)
- CS → GPIO8 (Pin 24)
- VDD & VREF → 3.3V
- AGND & DGND → GND

## Relay Module:
- DC+ → Pi 5V
- DC- → Pi GND
- IN → GPIO17 (Pin 11)
- COM → Pump Power +
- NO → Pump +
- Pump - → Power Ground

## Moisture Sensor:
- A0 → MCP3008 CH0
- VCC → 3.3V
- GND → GND
