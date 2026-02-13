
.. image:: https://img.shields.io/badge/Discord-Join%20our%20server-5865F2?style=for-the-badge&logo=discord&logoColor=white
    :target: https://discord.gg/mJxDjAM3PF
    :alt: Discord Server


.. image:: https://github.com/thingsboard/CircuitPython_thingsboard-client-sdk/workflows/Build%20CI/badge.svg
    :target: https://github.com/thingsboard/CircuitPython_thingsboard-client-sdk/actions
    :alt: Build Status


.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Code Style: Ruff

ThingsBoard CircuitPython Client SDK
====================================

**💡 Make the notion that it is the early alpha of MQTT client MicroPython SDK special for controllers. So we
appreciate any help in improving this project and getting it growing.**

ThingsBoard is an open-source IoT platform for data collection, processing, visualization, and device management.
This project is a CircuitPython library that provides convenient client SDK for Device API.

**SDK supports:**

- `Device MQTT <https://thingsboard.io/docs/reference/mqtt-api/>`_ API provided by ThingsBoard
- QoS 0 and 1
- Automatic reconnect
- Device Claiming

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/thingsboard-circuitpython-client-sdk/>`_.
To install for current user:

.. code-block:: shell

    pip3 install thingsboard-circuitpython-client-sdk

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install thingsboard-circuitpython-client-sdk

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install thingsboard-circuitpython-client-sdk

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install thingsboard-circuitpython-client-sdk

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Getting Started
===============

Client initialization and telemetry publishing

.. code-block:: python

import time

from tb_device_mqtt import TBDeviceMqttClient  # ThingsBoard MQTT client wrapper (your SDK)
import wifi  # CircuitPython Wi-Fi module

# Quick sanity-check that Wi-Fi is up before using MQTT
print("WiFi connected:", wifi.radio.connected)
print("IP:", wifi.radio.ipv4_address)

# ThingsBoard connection settings
HOST = "YOUR_HOST"            # e.g. "thingsboard.cloud" or "192.168.1.10"
PORT = "YOUR_PORT"            # e.g. 1883 (use an int if your client expects it)
TOKEN = "YOUR_ACCESS_TOKEN"   # device access token from ThingsBoard

# Telemetry payload to send (will appear in the device telemetry in ThingsBoard)
telemetry = {"temperature": 41.9, "enabled": False, "currentFirmwareVersion": "v1.2.2"}

# Create MQTT client instance
client = TBDeviceMqttClient(host=HOST, port=PORT, access_token=TOKEN)

try:
    print("Connecting...")
    client.connect()          # open MQTT connection to ThingsBoard
    time.sleep(1)             # small delay to ensure connection stabilizes on some boards

    print("Sending telemetry...")
    client.send_telemetry(telemetry)  # publish telemetry message
    time.sleep(1)             # allow time for message to be sent before disconnecting

finally:
    print("Disconnecting...")
    try:
        client.disconnect()   # close MQTT connection cleanly
    except Exception as e:
        # Prevent cleanup from crashing the script on disconnect issues
        print("Disconnect error:", e)




Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/thingsboard/CircuitPython_thingsboard-client-sdk/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Support
=======

 - `Join our Discord <https://discord.gg/mJxDjAM3PF>`_
 - `Community chat <https://gitter.im/thingsboard/chat>`_
 - `Stackoverflow <http://stackoverflow.com/questions/tagged/thingsboard>`_

Licenses
========

This project is released under `Apache 2.0 License <./LICENSE>`_.
