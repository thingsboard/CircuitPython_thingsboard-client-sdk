ThingsBoard CircuitPython Client SDK
====================================

.. image:: ./logo.png
    :alt: ThingsBoard Logo
    :align: center

.. class:: align-center

ThingsBoard is an open-source IoT platform for data collection, processing, visualization, and device management.
This project is a CircuitPython library that provides convenient client SDK for
`Device MQTT API <https://thingsboard.io/docs/reference/mqtt-api/>`_.


.. image:: https://github.com/thingsboard/CircuitPython_thingsboard-client-sdk/workflows/Build%20CI/badge.svg
    :target: https://github.com/thingsboard/CircuitPython_thingsboard-client-sdk/actions
    :alt: Build Status


.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Code Style: Ruff


.. image:: https://img.shields.io/badge/license-Apache_2.0-blue
    :target: https://github.com/thingsboard/CircuitPython_thingsboard-client-sdk/blob/main/LICENSE
    :alt: License: Apache 2.0


.. image:: https://img.shields.io/badge/contributions-welcome-green
    :target: https://github.com/thingsboard/CircuitPython_thingsboard-client-sdk/issues
    :alt: Contributions Welcome


.. image:: https://img.shields.io/github/v/release/thingsboard/CircuitPython_thingsboard-client-sdk
    :target: https://github.com/thingsboard/CircuitPython_thingsboard-client-sdk/releases/latest
    :alt: Release Version


.. image:: https://img.shields.io/discord/1458396495610122526?logo=discord
    :target: https://discord.gg/mJxDjAM3PF
    :alt: Discord Server

----

**💡 Make the notion that it is the early alpha of MQTT client MicroPython SDK special for controllers. So we
appreciate any help in improving this project and getting it growing.**


Table of Contents
=================

- `Features <#-features>`_
- `Dependencies <#-dependencies>`_
- `Installation <#-installation>`_

   - `PyPI <#installing-from-pypi>`_
   - `Circup <#installing-to-a-connected-circuitpython-device-with-circup>`_

- `Getting Started <#-getting-started>`_
- `Examples <#-examples>`_
- `Contributing <#-contributing>`_
- `Support & Community <#-support--community>`_
- `Licenses <#%EF%B8%8F-licenses>`_


🧩 Features
===========

- `Device MQTT <https://thingsboard.io/docs/reference/mqtt-api/>`_ API provided by ThingsBoard
- QoS 0 and 1
- Automatic reconnect
- Sending attributes to ThingsBoard.
- Sending telemetry data to ThingsBoard.
- Request client and shared attributes from ThingsBoard.
- Subscribing to attribute updates from ThingsBoard.
- Device claiming


🔗 Dependencies
===============

This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.


📦 Installation
===============

You can install the ThingsBoard CircuitPython Client SDK in several ways depending on your setup and preferences.


Installing from PyPI
--------------------

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
----------------------------------------------------------

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

🟢 Getting Started
==================

Client initialization and telemetry publishing

.. code-block:: python

    import time

    import wifi  # CircuitPython Wi-Fi module
    from tb_device_mqtt import TBDeviceMqttClient  # ThingsBoard MQTT client wrapper (your SDK)

    # Quick sanity-check that Wi-Fi is up before using MQTT
    print("WiFi connected:", wifi.radio.connected)
    print("IP:", wifi.radio.ipv4_address)

    # ThingsBoard connection settings
    HOST = "YOUR_HOST"  # e.g. "thingsboard.cloud" or "192.168.1.10"
    PORT = "YOUR_PORT"  # e.g. 1883 (use an int if your client expects it)
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


🪛 Examples
===========

You can find more examples `here <./examples>`_. They demonstrate how to use the SDK to connect to ThingsBoard, send
telemetry data, subscribe to attribute changes, handle RPC calls, etc.


⭐ Contributing
===============

We welcome contributions to the ThingsBoard CircuitPython Client SDK! If you have an idea for a new feature,
have found a bug, or want to improve the documentation, please feel free to submit a pull request or open an issue.
Please read our `Code of Conduct <./CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.


💬 Support & Community
======================

Need help or want to share ideas?

 - `Join our Discord <https://discord.gg/mJxDjAM3PF>`_
 - `Stackoverflow <http://stackoverflow.com/questions/tagged/thingsboard>`_

**🐞 Found a bug?** Please open an issue.


⚖️ Licenses
===========

This project is released under `Apache 2.0 License <./LICENSE>`_.
