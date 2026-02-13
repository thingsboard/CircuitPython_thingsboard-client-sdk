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

import gc
from json import dumps, loads

import socketpool
import wifi

__version__ = "0.0.1"
__repo__ = "https://github.com/samson0v/CircuitPython_thingsboard-client-sdk.git"

RPC_REQUEST_TOPIC = "v1/devices/me/rpc/request/"
RPC_RESPONSE_TOPIC = "v1/devices/me/rpc/response/"
ATTRIBUTES_TOPIC = "v1/devices/me/attributes"
ATTRIBUTE_REQUEST_TOPIC = "v1/devices/me/attributes/request/"
ATTRIBUTE_TOPIC_RESPONSE = "v1/devices/me/attributes/response/"
CLAIMING_TOPIC = "v1/devices/me/claim"


class TBDeviceMqttClient:
    def __init__(
        self,
        host,
        port=1883,
        access_token=None,
        quality_of_service=None,
        client_id=None,
    ):
        from adafruit_minimqtt.adafruit_minimqtt import MQTT

        gc.collect()

        self._host = host
        self._port = port
        self.quality_of_service = quality_of_service if quality_of_service is not None else 1
        self._attr_request_dict = {}
        self.__device_client_rpc_dict = {}
        self.__device_sub_dict = {}
        self.__device_on_server_side_rpc_response = None
        self.__attr_request_number = 0
        self.__device_client_rpc_number = 0
        self.__device_max_sub_id = 0
        self.__request_id = 0
        self.connected = False

        if not access_token:
            print("token is not set, connection without tls wont be established")
        self._access_token = access_token

        if not client_id:
            client_id = "sdk-client"
        self._client_id = client_id
        self._pool = socketpool.SocketPool(wifi.radio)

        self._client = MQTT(
            broker=self._host,
            port=self._port,
            client_id=self._client_id,
            username=self._access_token,
            password="pswd",
            keep_alive=120,
            socket_pool=self._pool,
        )

    def connect(self):
        try:
            response = self._client.connect()
            self._client.add_topic_callback("#", self.all_subscribed_topics_callback)

            self._client.subscribe(ATTRIBUTES_TOPIC, qos=self.quality_of_service)
            self._client.subscribe(ATTRIBUTES_TOPIC + "/response/+", qos=self.quality_of_service)
            self._client.subscribe(RPC_REQUEST_TOPIC + "+", qos=self.quality_of_service)
            self._client.subscribe(RPC_RESPONSE_TOPIC + "+", qos=self.quality_of_service)

            self.connected = True
            return response
        except Exception as e:
            self.connected = False
            print(f"Unexpected connection error: {e}", e)

    def disconnect(self):
        self._client.disconnect()
        self.connected = False

    def send_telemetry(self, data):
        telemetry_topic = "v1/devices/me/telemetry"
        self._client.publish(telemetry_topic, dumps(data))

    def send_attributes(self, data):
        self._client.publish(ATTRIBUTES_TOPIC, dumps(data))

    def request_attributes(self, client_keys=None, shared_keys=None, callback=None):
        msg = {}
        if client_keys:
            tmp = ""
            for key in client_keys:
                tmp += key + ","
            tmp = tmp[: len(tmp) - 1]
            msg.update({"clientKeys": tmp})
        if shared_keys:
            tmp = ""
            for key in shared_keys:
                tmp += key + ","
            tmp = tmp[: len(tmp) - 1]
            msg.update({"sharedKeys": tmp})
        self.__attr_request_number += 1
        self._attr_request_dict.update({self.__attr_request_number: callback})
        self._client.publish(
            ATTRIBUTE_REQUEST_TOPIC + str(self.__attr_request_number),
            dumps(msg),
            qos=self.quality_of_service,
        )

    def send_rpc_call(self, method, params, callback):
        self.__device_client_rpc_number += 1
        self.__device_client_rpc_dict.update({self.__device_client_rpc_number: callback})
        rpc_request_id = self.__device_client_rpc_number
        payload = {"method": method, "params": params}
        self._client.publish(
            RPC_REQUEST_TOPIC + str(rpc_request_id),
            dumps(payload),
            qos=self.quality_of_service,
        )

    def set_server_side_rpc_request_handler(self, handler):
        self.__device_on_server_side_rpc_response = handler

    def claim_device(self, secret_key=None, duration_ms=None):
        claim_request = {}
        if secret_key:
            claim_request["secretKey"] = secret_key
        if duration_ms:
            claim_request["durationMs"] = duration_ms

        payload = dumps(claim_request)
        print(f"Sending claim request to topic '{CLAIMING_TOPIC}' with payload: {payload}")
        self._client.publish(CLAIMING_TOPIC, payload, qos=self.quality_of_service)

    def clean_device_sub_dict(self):
        self.__device_sub_dict = {}

    def subscribe_to_all_attributes(self, callback):
        return self.subscribe_to_attribute("*", callback)

    def subscribe_to_attribute(self, key, callback):
        self.__device_max_sub_id += 1
        if key not in self.__device_sub_dict:
            self.__device_sub_dict.update({key: {self.__device_max_sub_id: callback}})
        else:
            self.__device_sub_dict[key].update({self.__device_max_sub_id: callback})
        print(f"Subscribed to {key} with id {self.__device_max_sub_id}")

        return self.__device_max_sub_id

    def unsubscribe_from_attribute(self, subscription_id):
        for attribute in self.__device_sub_dict:
            if self.__device_sub_dict[attribute].get(subscription_id):
                del self.__device_sub_dict[attribute][subscription_id]
                print(
                    "Unsubscribed from {0}, subscription id {1}".format(attribute, subscription_id)
                )
        if subscription_id == "*":
            self.__device_sub_dict = {}
        self.__device_sub_dict = dict((k, v) for k, v in self.__device_sub_dict.items() if v)

    def all_subscribed_topics_callback(self, topic, msg):
        topic = topic.decode("utf-8")
        print("callback", topic, msg)

        self._on_decode_message(topic, msg)

    def _on_decode_message(self, topic, msg):
        if topic.startswith(RPC_REQUEST_TOPIC):
            request_id = topic[len(RPC_REQUEST_TOPIC) : len(topic)]
            if self.__device_on_server_side_rpc_response:
                self.__device_on_server_side_rpc_response(request_id, loads(msg))
        elif topic.startswith(RPC_RESPONSE_TOPIC):
            request_id = int(topic[len(RPC_RESPONSE_TOPIC) : len(topic)])
            callback = self.__device_client_rpc_dict.pop(request_id)
            callback(request_id, loads(msg), None)
        elif topic == ATTRIBUTES_TOPIC:
            msg = loads(msg)
            dict_results = []

            if self.__device_sub_dict.get("*"):
                for subscription_id in self.__device_sub_dict["*"]:
                    dict_results.append(self.__device_sub_dict["*"][subscription_id])

            keys = msg.keys()
            keys_list = []
            for key in keys:
                keys_list.append(key)

            for key in keys_list:
                if self.__device_sub_dict.get(key):
                    for subscription in self.__device_sub_dict[key]:
                        dict_results.append(self.__device_sub_dict[key][subscription])
            for res in dict_results:
                res(msg, None)
        elif topic.startswith(ATTRIBUTE_TOPIC_RESPONSE):
            req_id = int(topic[len(ATTRIBUTES_TOPIC + "/response/") :])
            callback = self._attr_request_dict.pop(req_id)
            if isinstance(callback, tuple):
                callback[0](loads(msg), None, callback[1])
            else:
                callback(loads(msg), None)
