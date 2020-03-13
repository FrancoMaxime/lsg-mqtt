# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt 
import time
import requests
import threading
import serial
import matplotlib.pyplot as plt


BROKER_ADDRESS = "0.0.0.0"
ID_TRAY = "Plateau1"

class MyMQTTClass(mqtt.Client):
    def __init__(self, client_id, broker_address):
        mqtt.Client.__init__(self, client_id)
        self.capturing = False
        self.id_plateau = client_id
        self.broker_address = broker_address
        self.filename = None
        self.capturethread = CaptureThread(self)
        self.drink = []
        self.meal = []
        self.count = []

    def on_message(self, mqttc, obj, msg):
        data = msg.payload.decode("utf-8")
        data = data.split("\t")
        id = data[0]
        if id != self.id_plateau:
            if data[1] == "END MEAL":
                print("Starting end...")
                self.capturing = False
                url = 'http://' + BROKER_ADDRESS + ':5000/tray/data'
                
                print("Making plot...")
                self.make_plot()
                
                print("Sending to the server...")
                myfiles = {'data': open(self.filename ,'rb'), 'image': open(self.filename.split('.')[0]+'.png' ,'rb')}
                x = requests.post(url, files = myfiles)
                
                print("END MEAL")
                myfiles['data'].close()
                myfiles['image'].close()
                self.drink = []
                self.meal = []
                self.count = []
                self.filename = None
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
        
    def make_plot(self):
        plt.figure(figsize=(20, 10))
        plt.plot(self.count, self.drink, linewidth=0.50, label="Drink")
        plt.plot(self.count, self.meal, linewidth=0.50, label="Meal")
        plt.xlabel('Time')
        plt.ylabel('Weight')
        plt.title("Meal N°" + self.filename.split('.')[0])
        plt.legend()
        plt.savefig(self.filename.split('.')[0]+'.png')


class CaptureThread(threading.Thread):
    def __init__(self, config):
        threading.Thread.__init__(self)
        self.ser = None
        self.config = config

    def run(self):
        while True:
            if self.config.is_threading():
                if self.ser is None:
                    self.ser = serial.Serial(
                        port='/dev/ttyUSB0',
                        baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=1
                    )

                with open(self.config.filename , "a+")as f:
                    try:
                        x = self.ser.readline().decode('utf-8')
                        f.write("floup")
                        x = x.split("\t")
                        self.config.drink.append(float(x[1]))
                        self.config.meal.append(float(x[4]))
                        if len(self.config.count) == 0:
                            self.config.count.append(0.0)
                        else:
                            self.config.count.append(self.config.count[-1] + 1)
                            
                    finally:
                        time.sleep(1)
            else:
                self.ser = None
                time.sleep(1)
                

client = MyMQTTClass(ID_TRAY, BROKER_ADDRESS)
client.run()

while True:
    print("working....")
    time.sleep(30)
