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
HOST = "thingsboard.cloud"  # or your local TB host/IP
PORT = 1883  # standard MQTT port (non-TLS)
TOKEN = "YOUR_ACCESS_TOKEN"  # device access token from ThingsBoard

# Claiming settings
SECRET_KEY = "DEVICE_SECRET_KEY"  # key configured in the claiming widget
DURATION_MS = 30000  # how long the claim request is valid (ms)

client = None

try:
    # Create ThingsBoard MQTT client
    client = TBDeviceMqttClient(host=HOST, port=PORT, access_token=TOKEN)

    print("Connecting to ThingsBoard...")
    client.connect()
    print("Connected to ThingsBoard")

    # Send claiming request
    print("Sending claiming request...")
    client.claim_device(secret_key=SECRET_KEY, duration_ms=DURATION_MS)
    print("Claiming request was sent")

    # Keep the script alive for the claiming window
    # (so the device stays online while the claim is performed)
    time.sleep(DURATION_MS)

except Exception as e:
    print("Failed to execute device claiming:", e)

finally:
    # Disconnect cleanly
    if client is not None:
        try:
            client.disconnect()
        except Exception as e:
            print("Disconnect failed:", e)
    print("Connection closed")
