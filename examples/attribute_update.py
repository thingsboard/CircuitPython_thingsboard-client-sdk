# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2026 ThingsBoard Inc.
#
# SPDX-License-Identifier: Unlicense

import time

import wifi  # CircuitPython Wi-Fi module

from tb_device_mqtt import TBDeviceMqttClient  # ThingsBoard MQTT client wrapper (your SDK)

# Sanity check: Wi-Fi must be connected before MQTT
print("Connected:", wifi.radio.connected)
print("IP:", wifi.radio.ipv4_address)

# ThingsBoard connection settings
HOST = "YOUR_HOST"  # e.g. "thingsboard.cloud" or "192.168.1.10"
PORT = 1883  # standard MQTT port (non-TLS)
TOKEN = "YOUR_ACCESS_TOKEN"  # device access token from ThingsBoard
TIMEOUT = 20  # how long we keep pumping MQTT loop (seconds)

# Create and connect MQTT client
client = TBDeviceMqttClient(host=HOST, port=PORT, access_token=TOKEN)
client.connect()


def callback(result, *args):  # noqa: F841
    # Called when subscribed attribute update arrives
    # (extra args may contain metadata depending on your SDK design)
    print("Received data:", result)


# Subscribe to updates of a single attribute key (e.g. shared attribute "frequency")
sub_id = client.subscribe_to_attribute("frequency", callback)  # returns subscription id (optional)

# IMPORTANT: keep looping so incoming MQTT messages are processed
deadline = time.monotonic() + TIMEOUT
while time.monotonic() < deadline:
    client.check_for_msg()  # wraps MiniMQTT.loop() -> triggers callbacks
    time.sleep(0.05)  # small sleep to reduce CPU usage
