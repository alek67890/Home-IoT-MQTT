#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import time
from time import strftime,gmtime

t_list = ["28-000008fdc472"]      # One wire Address of Sensor

# Define Variables
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "Wroclaw/Sensors/Temp/Temp_1"
MQTT_MSG = ""


VERBOSE = True


def read_temp_from_sensor(thermometer):
        sensor_file = '/sys/bus/w1/devices/' + thermometer + '/w1_slave'
        t = open(sensor_file, 'r')
        lines = t.readlines()
        t.close()
        temp_output = lines[1].find('t=')
        if temp_output != -1:
                temp_string = lines[1].strip()[temp_output+2:]
                temp_c = float(temp_string)/1000.0
        return float(round(temp_c,1))

# Initiate MQTT Client
mqttc = mqtt.Client()

# Connect with MQTT Broker
mqttc.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
mqttc.subscribe(MQTT_TOPIC)
# mqttc.loop_start()

while True:
    current_temp = read_temp_from_sensor(t_list[0])
    data = str(current_temp) + " °C"
    data_time = strftime("%Y-%m-%d %H:%M:%S %Z", gmtime())
    if VERBOSE:
        print(data)
        print(data_time)
    mqttc.publish(MQTT_TOPIC, data, retain=True)
    mqttc.publish(MQTT_TOPIC + '/raw', current_temp, retain=True)
    mqttc.publish(MQTT_TOPIC + '/time', data_time, retain=True)
    time.sleep(29)

