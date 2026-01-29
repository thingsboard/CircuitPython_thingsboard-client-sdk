
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
PyPI <https://pypi.org/project/circuitpython-thingsboard-client-sdk/>`_.
To install for current user:

.. code-block:: shell

    pip3 install circuitpython-thingsboard-client-sdk

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install circuitpython-thingsboard-client-sdk

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
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
=============

Client initialization and telemetry publishing

.. code-block:: python

    from tb_device_mqtt import TBDeviceMqttClient
    telemetry = {"temperature": 41.9, "enabled": False, "currentFirmwareVersion": "v1.2.2"}
    client = TBDeviceMqttClient(host="127.0.0.1", port=1883, access_token="A1_TEST_TOKEN")
    # Connect to ThingsBoard
    client.connect()
    # Sending telemetry without checking the delivery status
    client.send_telemetry(telemetry)
    # Disconnect from ThingsBoard
    client.disconnect()

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/thingsboard/CircuitPython_thingsboard-client-sdk/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
