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

from adafruit_minimqtt.adafruit_minimqtt import MQTT, MMQTTException

from thingsboard_sdk.provision_client import ProvisionClient

from .sdk_core.device_mqtt import TBDeviceMqttClientBase

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/samson0v/CircuitPython_thingsboard-client-sdk.git"


class TBDeviceMqttClient(TBDeviceMqttClientBase):
    def __init__(
        self,
        host,
        port=1883,
        access_token=None,
        quality_of_service=None,
        client_id=None,
        chunk_size=0,
    ):
        super().__init__(host, port, access_token, quality_of_service, client_id, chunk_size)
        client = MQTT(
            broker=self._host,
            port=self._port,
            client_id=self._client_id,
            username=self._access_token,
            password="pswd",
            keep_alive=120,
        )
        self.set_client(client)

    def connect(self):
        try:
            response = self._client.connect()
            self._client.add_topic_callback("#", self.all_subscribed_topics_callback)

            self.__subscribe_all_required_topics()

            self.connected = True
            return response
        except MMQTTException as e:
            self.connected = False
            print(f"MQTT connection error: {e}")
        except Exception as e:
            self.connected = False
            print(f"Unexpected connection error: {e}", e)

    @staticmethod
    def provision(host, port, provision_request):
        provision_client = ProvisionClient(
            host=host, port=port, provision_request=provision_request
        )
        provision_client.provision()

        if provision_client.credentials:
            print("Provisioning successful. Credentilas obtained.")
            return provision_client.credentials
        else:
            print("Provisioning failed. No credentials obtained.")
            return None
