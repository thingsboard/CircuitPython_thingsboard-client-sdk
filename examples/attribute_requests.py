# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2026 ThingsBoard Inc.
#
# SPDX-License-Identifier: Unlicense

import time

import wifi  # CircuitPython Wi-Fi module

from tb_device_mqtt import TBDeviceMqttClient  # ThingsBoard MQTT client wrapper (your SDK)

# Sanity check: Wi-Fi must be connected before MQTT
print("WiFi connected:", wifi.radio.connected)
print("IP:", wifi.radio.ipv4_address)

# ThingsBoard connection settings
HOST = "YOUR_HOST"  # e.g. "thingsboard.cloud" or "192.168.1.10"
PORT = 1883  # standard MQTT port (non-TLS)
TOKEN = "YOUR_ACCESS_TOKEN"  # device access token from ThingsBoard
TIMEOUT = 20  # how long we keep pumping MQTT loop (seconds)

# Create and connect MQTT client
client = TBDeviceMqttClient(host=HOST, port=PORT, access_token=TOKEN)
client.connect()  # establishes MQTT session + subscriptions inside your SDK (if implemented)


def on_attributes_change(result, exception=None):
    # Callback is called when the attributes response arrives
    if exception is not None:
        print("Exception:", exception)
    else:
        print("Attributes response:", result)


# Request client/shared attributes by keys (your SDK forms attributes/request/<id>)
client.request_attributes(client_keys=["atr1", "atr2"], callback=on_attributes_change)

# IMPORTANT: CircuitPython needs a loop to receive/process MQTT packets
deadline = time.monotonic() + TIMEOUT
while time.monotonic() < deadline:
    client.check_for_msg()  # wraps MiniMQTT.loop() -> triggers callbacks
    time.sleep(0.05)  # small sleep to reduce CPU usage
