#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

# Define Variables
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "HomeLight/room1/light1"
MQTT_MSG = ""

# Configuration of GPIO
GPIO.setmode(GPIO.BCM)
LAMP = 21
BUTTON = 20
SWITCH = 26
GPIO.setup(LAMP, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN)
GPIO.setup(SWITCH, GPIO.IN)

# Print data or not
VERBOSE = True


class State:

    def __init__(self, state='off'):
        self.current = state

    def get(self):
        return self.current

    def set(self, state):
        self.current = state


def on_connect(mosq, obj, rc, op):
    if VERBOSE:
        print("Connected to MQTT Broker")
    mqttc.subscribe(MQTT_TOPIC)


def on_message(mosq, obj, msg):
    msq_dec = msg.payload.decode('UTF-8')
    try:
        obj.set(msq_dec)
        if VERBOSE:
            print(msg.topic)
            print(obj.get())
        if msq_dec == 'on':
            GPIO.output(LAMP, True)
        elif msq_dec == 'off':
            GPIO.output(LAMP, False)
    except:
        print("Error on Receive Message")
    finally:
        print(msq_dec)

# Initiate MQTT Client
mqttc = mqtt.Client()
state_of_lamp = State()
# Register Event Handlers
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.user_data_set(state_of_lamp)

# Connect with MQTT Broker
mqttc.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
mqttc.loop_start()
old_input_SWITCH = GPIO.input(SWITCH)
start_time = [time.strftime("%H:%M:%S")]

try:
    while True:  # Main Loop
        input_BUTTON = GPIO.input(BUTTON)
        if input_BUTTON == 1:

            if state_of_lamp.get() == 'on':
                state_of_lamp.set('off')
            else:
                state_of_lamp.set('on')
            MQTT_MSG = state_of_lamp.get()
            mqttc.publish(MQTT_TOPIC, MQTT_MSG, retain=True)
            while input_BUTTON:
                input_BUTTON = GPIO.input(BUTTON)
                time.sleep(0.001)
            time.sleep(0.1)

        input_SWITCH = GPIO.input(SWITCH)
        if input_SWITCH != old_input_SWITCH:

            if state_of_lamp.get() == 'on':
                state_of_lamp.set('off')
            else:
                state_of_lamp.set('on')
            MQTT_MSG = state_of_lamp.get()
            mqttc.publish(MQTT_TOPIC, MQTT_MSG, retain=True)
            old_input_SWITCH = input_SWITCH
            time.sleep(0.1)

        time.sleep(0.05)

except:
    if VERBOSE:
        print('Error !!!')
        print('Something in main loop is wrong')
        print(["Start Time -> ", start_time])
        print("Stop Time -> ", time.strftime("%H:%M:%S"))

finally:
    if VERBOSE:
        print('END')
    GPIO.cleanup()
    mqttc.disconnect()
