'''
ITWS3 PROJECT GROUP 12
RASBERRY PI CODE
LAST MODIFIED : Oct  13 03:22:38 IST 2017


'''
import RPi.GPIO as GPIO 
import time
from UUGear import *
'''
UUGear Library is used to connect Ardrino Board with Rasberry Pi Board.
Using Stack Protocol
'''
import requests         # Python Library to make HTTP requests
import sys, serial, threading   # Dependencies of UUGear Library
from subprocess import call     # Dependencies of UUGear Library
import datetime                 # Python Date-Time module
import os                       # Python operating system dependent module


UUGearDevice.setShowLogs(1)     # Initialisation Of Stack Protocol (setting up flags)

'''
We are currently using 2 Ardrino Boards
Thus conneting 2 Ardrino Boards with Rasberry PI
'''
device1 = UUGearDevice('UUGear-Arduino-6574-3279')      # Getting Ardrino 1 with device Id
device2 = UUGearDevice('UUGear-Arduino-1783-1825')      # Getting Ardrino 2 with device Id


GPIO.setmode(GPIO.BCM) #Broadcom SOC channel (In simple words Its a specific Config. of pins in Rasberry Pi)
#Initialisation Of GPIO Pins
TRIG = 23
ECHO = 24
RELAY1 = 25
RELAY2 = 27
acc1,acc2 = 0,0
# Setting Up the Pin Status
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(RELAY1,GPIO.OUT)
GPIO.setup(RELAY2,GPIO.OUT)
GPIO.output(TRIG, False)

'''
Setting Up GPIO Pins for Actuators
RELAY1  will trigger the relay of actuator 1
RELAY2  will trigger the relay of actuator 2
'''
print "Pump1 off"
acc1 = 0
GPIO.output(RELAY1, True)
print "Pump2 off"
acc2 = 0
GPIO.output(RELAY2, True)

while(True):

        temperature = 0
        soil_moisture1 = 0
        soil_moisture2 = 0
        ldr,rain_gauge1 = 0
        rain_gauge2 = 0
        
        '''
        Using Ultrasonic Sensor for Water Level of Water Tank.
        This sensor is controlled by Rasberry Pi.
        Thus GPIO Pins are used.
        '''
	GPIO.output(TRIG, True)        #Triggering Ultra Sonic wave
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
                                        
	if GPIO.input(ECHO)==0:
                pulse_start = time.time() #Initialising Start Time

	while GPIO.input(ECHO)==1:
                pulse_end = time.time() #Getting echo back

	pulse_duration = pulse_end - pulse_start
	distance = round(pulse_duration * 17150, 2)
	print "Distance:",distance,"cm"        # Water Tank Empty Part

        
        #Gatting Data from Ardrino 1 sensors
        if device1.isValid():            #Checking for validity
                print 'Device 1 is ready'
                temperature = device1.analogRead(1)*0.40020125
                print "%0.2f" % temperature
                time.sleep(0.1)
        
        else:
                print 'Device 1 is not ready.'

        #Gatting Data from Ardrino 1 sensors
        if device2.isValid():                   #Checking for validity
                print 'Device 2 is ready'

                soil_moisture1 = device2.analogRead(1)
                print "soil_moisture1: ",soil_moisture1
                time.sleep(0.1)

                soil_moisture2 = device2.analogRead(4)
                print "soil_moisture2: ",soil_moisture2
                time.sleep(0.1)

                '''
                        Rain Gauge is Implemented By water level sensor
                        Here Readings of Water Level Sensor is Converted to millimeter scale
                        This way will give better results then
                                                        rain_gauge1 = map(rain_gauge1,480,705,0,40) 
                '''
                rain_gauge1 = device2.analogRead(5)
                if rain_gauge1<=480:
                        rain_gauge1 = 0
                elif (rain_gauge1>480 and rain_gauge1<=530): 
                        rain = 3
                elif (rain_gauge1>530 and rain_gauge1<=615): 
                        rain_gauge1 = 8
                elif (rain_gauge1>615 and rain_gauge1<=660): 
                        rain_gauge1 = 13
                elif (rain_gauge1>660 and rain_gauge1<=680): 
                        rain_gauge1 = 18
                elif (rain_gauge1>680 and rain_gauge1<=690): 
                        rain_gauge1 = 23
                elif(rain_gauge1>690 and rain_gauge1<=700): 
                        rain_gauge1 = 28
                elif (rain_gauge1>700 and rain_gauge1<=705): 
                        rain_gauge1 = 33 
                elif(rain_gauge1>705): 
                        rain_gauge1 = 38
                print "rain_gauge1: ",rain_gauge1
                time.sleep(0.1)

                rain_gauge2 = device2.analogRead(3)
                if (rain_gauge2<=480):
                	rain_gauge2 = 0
                elif (rain_gauge2>480 and rain_gauge2<=530): 
                        rain_gauge2 = 3
                elif (rain_gauge2>530 and rain_gauge2<=615): 
                        rain_gauge2 = 8
                elif (rain_gauge2>615 and rain_gauge2<=660): 
                        rain_gauge2 = 13
                elif (rain_gauge2>660 and rain_gauge2<=680): 
                        rain_gauge2 = 18
                elif (rain_gauge2>680 and rain_gauge2<=690): 
                        rain_gauge2 = 23
                elif(rain_gauge2>690 and rain_gauge2<=700): 
                        rain_gauge2 = 28
                elif (rain_gauge2>700 and rain_gauge2<=705): 
                        rain_gauge2 = 33 
                elif(rain_gauge2>705): 
                        rain_gauge2 = 38
                print "rain_gauge2: ",rain_gauge2
                time.sleep(0.1)

                ldr = device2.analogRead(2)
                print "LDR: ",ldr               #LDR sensor is used to measure sunlight intensity
                time.sleep(0.1)
        else:
                print 'Device 2 is not ready.'


        if (distance > 10 or soil_moisture1 < 700) or rain_gauge1 > 5:
                print "pump off"
                acc1 = 0
                GPIO.output(RELAY1, True)
        elif distance < 10 and soil_moisture1 > 700 and rain_gauge1 <= 5:
                print "pump on"
                acc1 = 1
                GPIO.output(RELAY1, False)
        elif distance < 10 and soil_moisture1 > 500 and ldr > 800 and rain_gauge1 <= 5:
                print "pump on"
                acc1 = 1
                GPIO.output(RELAY1, False)
        
        if (distance > 10 or soil_moisture2 < 700) or rain_gauge2 > 5:
                print "pump off"
                acc2 = 0
                GPIO.output(RELAY2, False)
        elif distance < 10 and soil_moisture2 > 700 and rain_gauge2 <= 5:
                print "pump on"
                acc2 = 1
                GPIO.output(RELAY2, True)
        elif distance < 10 and soil_moisture2 > 500 and ldr > 800 and rain_gauge2 <= 5:
                print "pump on"
                acc2 = 1
                GPIO.output(RELAY2, True)

        '''
        We have hosted our Django server on 
                                        1.Python Anywhere
                                        2. IIIT Server
        Here We are Posting the data to Django server(cloud)
        sId like "cefccad6-ae42-4fca-baed-7a1cae10dce7" are the sensor ids which we generated in Django with UUid module
        This id is Unique of each sensor of each plant
        content is the JSON response which we get from the Django server every time we post HTTP response

        Here Sleep time is necessary because of network connection issues and other factors
        So Total Time taken just to post readings in one round is aprox 6 seconds
        '''
        if 1 :          #Plant1
                post_data = {'sID':"cefccad6-ae42-4fca-baed-7a1cae10dce7",'value': float(temperature)}
                #response = requests.post('https://anuragiiit.pythonanywhere.com/addtemperaturereading/', data=post_data)
                response = requests.post('https://jeet007.pythonanywhere.com/sensor/adddata/', data=post_data)  
                #response = requests.post('http://10.0.3.23:8080/sensor/adddata/', data=post_data)
                content = response.content
		print("Temperature Plant1: ",temperature,content)
	time.sleep(0.05)
	if 2 :         #Plant2
                post_data = {'sID':"6db7e9b1-9d45-4b64-adad-985bba42dfe8",'value': float(temperature)}
                #response = requests.post('https://anuragiiit.pythonanywhere.com/addtemperaturereading/', data=post_data)
                response = requests.post('https://jeet007.pythonanywhere.com/sensor/adddata/', data=post_data)
                #response = requests.post('http://10.0.3.23:8080/sensor/adddata/', data=post_data)
                content = response.content
		print("Temperature Plant2: ",temperature,content)
	time.sleep(0.05)

	if 1 :
                post_data = {'sID':"d15d9e11-9c70-4db7-be44-50df8d8ce2de",'value': (100-(distance*100/13))}#Plant1
                #response = requests.post('https://anuragiiit.pythonanywhere.com/addtemperaturereading/', data=post_data)
                response = requests.post('https://jeet007.pythonanywhere.com/sensor/adddata/', data=post_data)
                #response = requests.post('http://10.0.3.23:8080/sensor/adddata/', data=post_data)
                content = response.content
		print("WaterLevel Plant1: ",(100-(100*distance/13)),content)  #Water Tank Water Part
        time.sleep(0.05)
        if 2 :
                post_data = {'sID':"bc4bee0f-80e3-4a85-9b6a-c8f563523fd2",'value': (100-(distance*100/13))}
                #response = requests.post('https://anuragiiit.pythonanywhere.com/addtemperaturereading/', data=post_data)
                response = requests.post('https://jeet007.pythonanywhere.com/sensor/adddata/', data=post_data)
                #response = requests.post('http://10.0.3.23:8080/sensor/adddata/', data=post_data)
                content = response.content
		print("WaterLevel Plant2: ",(100-(100*distance/13)),content)  #Water Tank Water Part
        time.sleep(0.05)

	if 1 :
                post_data = {'sID':"21dafae7-78e2-4b66-9a27-7ea507d65cce",'value': (100-soil_moisture1/12.0)}#plant1
                #response = requests.post('https://anuragiiit.pythonanywhere.com/addtemperaturereading/', data=post_data)
                response = requests.post('https://jeet007.pythonanywhere.com/sensor/adddata/', data=post_data)
                #response = requests.post('http://10.0.3.23:8080/sensor/adddata/', data=post_data)
                content = response.content
		print("SoilMoisture Plant1: ",(100-soil_moisture1/12.0),content)
	time.sleep(0.05)	
        if 2 :
                post_data = {'sID':"f1635e70-30c9-4630-8ee0-dbc52e1eb481",'value': (100-soil_moisture2/12.0)}
                #response = requests.post('https://anuragiiit.pythonanywhere.com/addtemperaturereading/', data=post_data)
                response = requests.post('https://jeet007.pythonanywhere.com/sensor/adddata/', data=post_data)
                #response = requests.post('http://10.0.3.23:8080/sensor/adddata/', data=post_data)
                content = response.content
		print("SoilMoisture Plant2: ",(100-soil_moisture2/12.0),content)
	time.sleep(0.05)	

        if 1 :
                post_data = {'sID':"c6e692aa-d3d0-47df-8bca-eefd22920cbc",'value': ldr}
                #response = requests.post('https://jeet007.pythonanywhere.com/sensor/adddata/', data=post_data)
                response = requests.post('https://jeet007.pythonanywhere.com/sensor/adddata/', data=post_data)
                #response = requests.post('http://10.0.3.23:8080/sensor/adddata/', data=post_data)
                content = response.content
		print("SunLight Plant1: ",ldr,content)
	time.sleep(0.05)
	if 2 :
                post_data = {'sID':"3fa9b862-1b89-4c8d-80a5-f63f2a11b617",'value': ldr}
                #response = requests.post('https://jeet007.pythonanywhere.com/sensor/adddata/', data=post_data)
                response = requests.post('https://jeet007.pythonanywhere.com/sensor/adddata/', data=post_data)
                #response = requests.post('http://10.0.3.23:8080/sensor/adddata/', data=post_data)
                content = response.content
		print("SunLight Plant2: ",ldr,content)
	time.sleep(0.05)

        if 1 :
                post_data = {'sID':"fe5a1c45-fb2f-4a71-b4cc-4aafa68b789d",'value': rain_gauge1}
                #response = requests.post('https://jeet007.pythonanywhere.com/sensor/adddata/', data=post_data)
                response = requests.post('https://jeet007.pythonanywhere.com/sensor/adddata/', data=post_data)
                #response = requests.post('http://10.0.3.23:8080/sensor/adddata/', data=post_data)
                content = response.content
		print("RainGauge Plant1: ",rain_gauge1,content)
	time.sleep(0.05)	
        if 2 :
                post_data = {'sID':"d2844c29-2e1a-449b-881a-19f10595016c",'value': rain_gauge2}
                #response = requests.post('https://jeet007.pythonanywhere.com/sensor/adddata/', data=post_data)
                response = requests.post('https://jeet007.pythonanywhere.com/sensor/adddata/', data=post_data)
                #response = requests.post('http://10.0.3.23:8080/sensor/adddata/', data=post_data)
                content = response.content
		print("RainGauge Plant2: ",rain_gauge2,content)
	time.sleep(0.05)	
        

        if 1 :
                post_data = {'name':"plant1",'value': acc1}
                #response = requests.post('https://jeet007.pythonanywhere.com/sensor/adddata/', data=post_data)
                response = requests.post('https://jeet007.pythonanywhere.com/sensor/adddata/', data=post_data)
                #response = requests.post('http://10.0.3.23:8080/sensor/adddata/', data=post_data)
                content = response.content
		print("Acctuator Plant1: ",acc1,content)
	time.sleep(0.05)	
        if 2 :
                post_data = {'name':"plant2",'value': acc2}
                #response = requests.post('https://jeet007.pythonanywhere.com/sensor/adddata/', data=post_data)
                response = requests.post('https://jeet007.pythonanywhere.com/sensor/adddata/', data=post_data)
                #response = requests.post('http://10.0.3.23:8080/sensor/adddata/', data=post_data)
                content = response.content
		print("Acctuator Plant2: ",acc2,content)
	time.sleep(0.05)	

device1.detach()        # Break Connection Between RasberryPI and Ardrino
device1.stopDaemon()    # Stop all the running processes
device2.detach()
device2.stopDaemon()
GPIO.cleanup()          # Reset GPIO pins