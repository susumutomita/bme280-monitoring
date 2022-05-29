#!/usr/bin/env python3
"""
Requirement
1. Raspberry Pi OS, Python3
2. Enable I2C in Raspberry pi
"""

import cgsensor  # インポート
import influxdb
import datetime
import schedule
import time


def get_data():
    bme280 = cgsensor.BME280(i2c_addr=0x77)
    bme280.forced()
    return {
        "temperature": bme280.temperature,
        "humidity": bme280.humidity,
        "pressure": bme280.pressure,
    }


db = influxdb.InfluxDBClient(host="localhost", port=8086, database="sensor")


def write_to_influxdb(data):
    json_body = [
        {
            "measurement": "sensor",
            "time": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "fields": data,
        }
    ]
    print(json_body)
    db.write_points(json_body)


def on_minute():
    data = get_data()
    write_to_influxdb(data)


def main():
    schedule.every(1).minutes.do(on_minute)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
