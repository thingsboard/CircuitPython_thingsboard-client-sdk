# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2026 ThingsBoard Inc.
#
# SPDX-License-Identifier: Unlicense

import os
import time

import wifi  # CircuitPython Wi-Fi module

from tb_device_mqtt import TBDeviceMqttClient  # ThingsBoard MQTT client wrapper (your SDK)

# Quick sanity-check that Wi-Fi is up before using MQTT
print("WiFi connected:", wifi.radio.connected)
print("IP:", wifi.radio.ipv4_address)

# ThingsBoard connection settings
HOST = "YOUR_HOST"  # e.g. "thingsboard.cloud" or "192.168.1.10"
PORT = 1883  # e.g. 1883 (use an int if your client expects it)
TOKEN = "YOUR_ACCESS_TOKEN"  # device access token from ThingsBoard
RPC_METHODS = ("Pwd", "Ls")


# Create MQTT client instance
client = TBDeviceMqttClient(host=HOST, port=PORT, access_token=TOKEN)


def on_server_side_rpc_request(request_id, request_body):
    # request_id: numeric id from the MQTT topic
    # request_body: decoded JSON dict, typically {"method": "...", "params": ...}
    print("[RPC] id:", request_id, "body:", request_body)

    # Validate incoming payload type
    if not isinstance(request_body, dict):
        print("[RPC] bad request format (not a dict)")
        return

    # Extract method name and parameters from the RPC payload
    method = request_body.get("method")
    params = request_body.get("params")

    if method not in RPC_METHODS:
        reply = {"error": "Unsupported method", "method": method}
        # Send RPC response back to ThingsBoard (method name depends on your SDK wrapper)
        client.send_rpc_reply(request_id, reply)
        return

    # RPC: "Pwd" - return current working directory on the device filesystem
    if method == "Pwd":
        reply = {"current_directory": os.getcwd()}
        client.send_rpc_reply(request_id, reply)

    # RPC: "Ls" - list files in a directory
    elif method == "Ls":
        try:
            # If params is missing/empty, default to root ("/") or current dir
            if not params:
                params = "/"
            # Here we treat params directly as a path string for simplicity.
            files = os.listdir(params)
            reply = {"path": params, "files": files}
            client.send_rpc_reply(request_id, reply)
        except Exception as e:
            reply = {"error": str(e)}
            client.send_rpc_reply(request_id, reply)


client = TBDeviceMqttClient(HOST, port=PORT, access_token=TOKEN)
# Register the server-side RPC callback before the main loop
client.set_server_side_rpc_request_handler(on_server_side_rpc_request)
# Connect to ThingsBoard
client.connect()

# Main loop (non-blocking)
while True:
    # Non-blocking: poll for incoming MQTT packets
    client.check_for_msg()
    time.sleep(0.1)  # small delay to avoid busy-waiting (adjust as needed)
