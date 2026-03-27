# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2026 ThingsBoard Inc.
#
# SPDX-License-Identifier: Unlicense

import time

import adafruit_sht31d
import adafruit_ssd1306
import board
import busio
import requests

from tb_device_mqtt import TBDeviceMqttClient

THINGSBOARD_HOST = "YOUR_THINGSBOARD_HOST"
THINGSBOARD_TOKEN = "YOUR_THINGSBOARD_DEVICE_TOKEN"
THINGSBOARD_PORT = 1883

OPENWEATHER_API_KEY = "YOUR_WEATHER_API_KEY"
DEFAULT_CITY = "Kyiv,UA"

WEATHER_UPDATE_PERIOD = 600
DISPLAY_REFRESH_PERIOD = 2
TELEMETRY_SEND_PERIOD = 10

selected_city = DEFAULT_CITY

i2c = busio.I2C(board.SCL, board.SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
sensor = adafruit_sht31d.SHT31D(i2c)


def draw_screen(indoor_temp, indoor_humidity, outdoor_temp, outdoor_humidity):
    display.fill(0)

    display.text(f"InT:{indoor_temp:5.1f}C", 0, 0, 1)
    display.text(f"InH:{indoor_humidity:5.1f}%", 64, 0, 1)

    if outdoor_temp is not None:
        display.text(f"OutT:{outdoor_temp:4.1f}C", 0, 16, 1)
    else:
        display.text("OutT: N/A", 0, 16, 1)

    if outdoor_humidity is not None:
        display.text(f"OutH:{outdoor_humidity:4.1f}%", 64, 16, 1)
    else:
        display.text("OutH: N/A", 64, 16, 1)

    display.show()


def get_current_weather(city_name):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": OPENWEATHER_API_KEY, "units": "metric"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            "temp": float(data["main"]["temp"]),
            "humidity": float(data["main"]["humidity"]),
        }
    except Exception as e:
        print("Weather request failed:", e)
        return None


def main():
    weather_data = {"temp": None, "humidity": None}

    last_weather_update = 0.0
    last_display_refresh = 0.0
    last_telemetry_send = 0.0

    client = TBDeviceMqttClient(
        THINGSBOARD_HOST, port=THINGSBOARD_PORT, access_token=THINGSBOARD_TOKEN
    )
    client.connect()

    initial_weather = get_current_weather(selected_city)
    if initial_weather is not None:
        weather_data["temp"] = initial_weather["temp"]
        weather_data["humidity"] = initial_weather["humidity"]

    while True:
        now = time.monotonic()

        indoor_temp = sensor.temperature
        indoor_humidity = sensor.relative_humidity

        if now - last_weather_update >= WEATHER_UPDATE_PERIOD:
            last_weather_update = now
            updated_weather = get_current_weather(selected_city)
            if updated_weather is not None:
                weather_data["temp"] = updated_weather["temp"]
                weather_data["humidity"] = updated_weather["humidity"]

        if now - last_display_refresh >= DISPLAY_REFRESH_PERIOD:
            last_display_refresh = now
            draw_screen(
                indoor_temp, indoor_humidity, weather_data["temp"], weather_data["humidity"]
            )

        if now - last_telemetry_send >= TELEMETRY_SEND_PERIOD:
            last_telemetry_send = now

            telemetry = {
                "indoorTemp": round(indoor_temp, 1),
                "indoorHumidity": round(indoor_humidity, 1),
                "outdoorTemp": weather_data["temp"],
                "outdoorHumidity": weather_data["humidity"],
                "city": selected_city,
            }

            try:
                client.send_telemetry(telemetry)
                print("Telemetry sent:", telemetry)
            except Exception as e:
                print("Telemetry send failed:", e)

        time.sleep(0.1)


if __name__ == "__main__":
    main()
