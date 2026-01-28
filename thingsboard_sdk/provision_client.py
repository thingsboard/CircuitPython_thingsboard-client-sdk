# SPDX-FileCopyrightText: 2026 ThingsBoard
#
# SPDX-License-Identifier: Apache-2.0

"""
`thingsboard_sdk.tb_device_mqtt`
================================================================================

ThingsBoard CircuitPython client SDK


* Author(s): Vitalii Bidochka

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
"""

from adafruit_minimqtt.adafruit_minimqtt import MQTT

from .sdk_core.provision_client import ProvisionClientBase

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/samson0v/CircuitPython_thingsboard-client-sdk.git"


class ProvisionClient(ProvisionClientBase):
    def __init__(self, host, port, provision_request):
        super().__init__(host, port, provision_request)

        client = MQTT(
            client_id=str(self._client_id), broker=self._host, port=self._port, keep_alive=10
        )
        client.add_topic_callback(
            str(ProvisionClientBase.PROVISION_RESPONSE_TOPIC), self.on_message_callback
        )
        self.set_client(client)

    def provision(self):
        try:
            return super().provision()
        finally:
            if self._client:
                self._client.disconnect()
