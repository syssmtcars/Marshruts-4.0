#!/usr/bin/env python3

import time
from ev3dev.ev3 import *
from time import sleep
import math
import paho.mqtt.client as mqtt

mB = MediumMotor('outA')
mC = MediumMotor('outD')
msgFromPC = ""

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("center")


def on_message(client, userdata, msg):
    global msgFromPC
    msgFromPC = msg.payload.decode()
    print(msgFromPC)


client = mqtt.Client()
client.connect("192.168.0.34", 1883, 60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
