#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import paho.mqtt.client as mqtt
import time
import threading
from time import strftime,gmtime

# Define Variables
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "Wroclaw/Sensors/Temp/Temp_1/raw"
MQTT_MSG = ""


VERBOSE = True


class CurrentTemp:
    def __init__(self, temp=9999):
        self.CurrentTemperature = temp

    def set(self, temp):
        self.CurrentTemperature = temp

    def get(self):
        return self.CurrentTemperature

    def get_str(self):
        return str(self.CurrentTemperature)


def on_connect(mosq, obj, rc, op):
    if VERBOSE:
        print("Connected to MQTT Broker")
    mqttc.subscribe(MQTT_TOPIC)


def on_message(mosq, obj, msg):
    msq_dec = "Nie liczba"
    # msg.topic
    try:
        msq_dec = float(msg.payload.decode('UTF-8'))
        obj.set(msq_dec)
        if VERBOSE:
            print(msg.topic)
            # print(obj.get_str())
    except:
        print("Error on Receive Message")
    finally:
        print(msq_dec)
        pass

# def read_temp_from_file(thermometer):
#         sensor_file = '/sys/bus/w1/devices/' + thermometer + '/w1_slave'
#         t = open(sensor_file, 'r')
#         lines = t.readlines()
#         t.close()
#         temp_output = lines[1].find('t=')
#         if temp_output != -1:
#                 temp_string = lines[1].strip()[temp_output+2:]
#                 temp_c = float(temp_string)/1000.0
#         return float(round(temp_c,1))


def save_to_file(txt):
    with open('./pycharm/TempSensors/Data/temp_1_log.csv', 'a') as f:
            w = csv.writer(f)
            w.writerow(txt)


# class PeriodicExecutor(threading.Thread):
#     def __init__(self, sleep, func, params):
#         """ execute func(params) every 'sleep' seconds """
#         self.func = func
#         self.params = params
#         self.sleep = sleep
#         threading.Thread.__init__(self, name="PeriodicExecutor")
#         self.setDaemon(1)
#
#     def run(self):
#         while 1:
#             time.sleep(self.sleep)
#             apply(self.func, self.params)


def save_step(objectTemp):
    temp = objectTemp.get()
    if temp != 9999:
        print('log create')
        c = '°C'
        data2 = [temp, c, strftime("%Y-%m-%d , %H:%M:%S %Z", gmtime())]
        save_to_file(data2)


# Initiate MQTT Client
mqttc = mqtt.Client()

objectTemp = CurrentTemp()
# Register Event Handlers
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.user_data_set(objectTemp)

# Connect with MQTT Broker
mqttc.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
mqttc.loop_start()


# while ((int(strftime("%S", gmtime())) != 0 )or ((int(strftime("%M", gmtime())) % 10) != 0)):
#     pass
#
# print(strftime("%M    :    %S", gmtime()))
# save_step(objectTemp)
# loop = PeriodicExecutor(600, save_step, [objectTemp])
# loop.run()

while True:
    # int(strftime("%S", gmtime())) == 0 and
    if (int(strftime("%M", gmtime())) % 10) == 0:
        save_step(objectTemp)
        time.sleep(60)
    time.sleep(0.2)



