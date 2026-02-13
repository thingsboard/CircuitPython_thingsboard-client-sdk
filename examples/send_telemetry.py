# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2026 ThingsBoard Inc.
#
# SPDX-License-Identifier: Unlicense

import time

import wifi  # CircuitPython Wi-Fi module

from tb_device_mqtt import TBDeviceMqttClient  # ThingsBoard MQTT client wrapper (your SDK)

# Quick sanity-check that Wi-Fi is up before using MQTT
print("WiFi connected:", wifi.radio.connected)
print("IP:", wifi.radio.ipv4_address)

# ThingsBoard connection settings
HOST = "YOUR_HOST"  # e.g. "thingsboard.cloud" or "192.168.1.10"
PORT = "YOUR_PORT"  # e.g. 1883 (use an int)
TOKEN = "YOUR_ACCESS_TOKEN"  # device access token from ThingsBoard

# Telemetry payload to send (will appear in the device telemetry in ThingsBoard)
telemetry = {"temperature": 41.9, "enabled": False, "currentFirmwareVersion": "v1.2.2"}

# Create MQTT client instance
client = TBDeviceMqttClient(host=HOST, port=PORT, access_token=TOKEN)

try:
    print("Connecting...")
    client.connect()  # open MQTT connection to ThingsBoard
    time.sleep(1)  # small delay to ensure connection stabilizes on some boards

    print("Sending telemetry...")
    client.send_telemetry(telemetry)  # publish telemetry message
    time.sleep(1)  # allow time for message to be sent before disconnecting

finally:
    print("Disconnecting...")
    try:
        client.disconnect()  # close MQTT connection cleanly
    except Exception as e:
        # Prevent cleanup from crashing the script on disconnect issues
        print("Disconnect error:", e)
