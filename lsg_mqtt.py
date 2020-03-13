# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt 
import time
import requests
import threading

BROKER_ADDRESS = "localhost"
ID_TRAY = "Plateau1"

class MyMQTTClass(mqtt.Client):
    def __init__(self, client_id, broker_address):
        mqtt.Client.__init__(self, client_id)
        self.capturing = False
        self.id_plateau = client_id
        self.broker_address = broker_address
        self.serial = None
        self.filename = None
        self.capturethread = CaptureThread(self)

    def on_message(self, mqttc, obj, msg):
        data = msg.payload.decode("utf-8")
        data = data.split("\t")
        id = data[0]
        if id != self.id_plateau:
            if data[1] == "END MEAL":
                self.capturing = False
                url = 'http://0.0.0.0:5000/tray/data'
                myfiles = {'data': open(self.filename ,'rb')}
                x = requests.post(url, files = myfiles)
                print(x)
                print("END MEAL")
                myfiles['data'].close()
            elif data[1] == "START MEAL":
                self.capturing = True
                self.filename = data[2]
                print("START MEAL")
            else:
                print("Nothing to do")

    def run(self):
        self.connect(self.broker_address, 1883, 60)
        self.subscribe("lsg/" + self.id_plateau.lower(), 0)
        self.loop_start()
        self.capturethread.start()
        
    def is_threading(self):
        return self.capturing


class CaptureThread(threading.Thread):
    def __init__(self, config):
        threading.Thread.__init__(self)
        self.ser = None
        self.config = config

    def run(self):
        if self.config.is_threading() and seld.ser is None:
            """self.ser = serial.Serial(
                port='/dev/ttyUSB0',
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
            )"""
            
        while True:
            if self.config.is_threading():
                with open(self.config.filename , "a+")as f:
                    """x = self.ser.readline().decode('utf-8')"""
                    f.write("floup")
                    time.sleep(1)
                

client = MyMQTTClass(ID_TRAY, BROKER_ADDRESS)
client.run()

while True:
    print("working....")
    time.sleep(30)
