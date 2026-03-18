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
HOST = "YOUR_HOST"  # or your local TB host/IP
PORT = 1883  # 1883 = MQTT (no TLS)
TOKEN = "YOUR_ACCESS_TOKEN"  # token of the device you want to claim

# Claiming settings
SECRET_KEY = "DEVICE_SECRET_KEY"  # key configured in the claiming widget
DURATION_MS = 30000  # how long the claim request is valid (ms)

# Create client and connect
client = TBDeviceMqttClient(host=HOST, port=PORT, access_token=TOKEN)

print("Connecting to ThingsBoard...")
client.connect()

# Send claiming request
print("Sending claiming request...")
client.claim_device(secret_key=SECRET_KEY, duration_ms=DURATION_MS)

# Give MQTT some time to send packets (CircuitPython needs loop pumping)
deadline = time.monotonic() + 5
while time.monotonic() < deadline:
    client.check_for_msg()  # processes incoming packets (if any) and keeps connection alive
    time.sleep(0.05)

print("Done. If the secret key is correct, the device should be claimed in ThingsBoard.")
client.disconnect()
