#device libraries
import sys
import RPi.GPIO as GPIO
from gpiozero import Button
from time import sleep 
import datetime as datetime
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from rpi_lcd import LCD
lcd = LCD()

#Soil setup
soil = Button(24)

#amazonaws host and certs
host = "a3f69y8dukmi8a-ats.iot.us-east-1.amazonaws.com"
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"

#mqtt connection
my_rpi = AWSIoTMQTTClient("farm1-irrigation")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec

def activation():
    try:
        publisher()
        lcd.text('Soil is dry',1)
        lcd.text('Pump Turned ON',2)
        print("Soil moisture is dry.. Pump will be turned on")
        print("turning on pump, watering for 1 seconds..") 
        watering()
        sleep(1)
        closewater()
        print("pump turning off")
        sleep(2)
        #Check moisture reading again
        lcd.text('Checking soil',1)
        lcd.text('Moisture',2)
        print("Checking soil moisture again..")
    except Exception as e: 
        print(e)
        print('error')
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])

def publisher():
    try:
        import datetime as datetime
        import json
        message = {}
        message["deviceid"] = "farm1"
        now = datetime.datetime.now()
        message["datetime_value"] = now.strftime("%d/%m/%Y, %H:%M:%S")
        message["activate"] = 1		
        my_rpi.publish("farm/pump", json.dumps(message), 1)
    except Exception as e: 
        print(e)
        print('error')
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        
def watering():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23,GPIO.OUT)
    GPIO.output(23,GPIO.HIGH)
    
def closewater():
    GPIO.setup(23,GPIO.LOW)
    GPIO.setup(23,GPIO.IN)

def pumpCallback(client, userdata, message):
        print('reach pumpCallback')
        data = json.loads(message.payload)
        if data['turn'] == 'On':
            publisher()
            watering()
        elif data['turn'] == 'Off':
            closewater()
            
my_rpi.connect()
my_rpi.subscribe("farm/pump/farm1", 1, pumpCallback)
print("Successfully connected to MQTT!")

update = True
while update:
    try:
        lcd = LCD()
        if soil.is_held:
            lcd.text('Soil is wet',1)
            lcd.text('Pump OFF',2)
            print("Soil moisture is wet, Pump is not turned on")
            sleep(10)
            print("Checking Soil moisture after 10 seconds...")
            sleep(5)
        else:
            activation()
            sleep(3)

    except Exception as e: 
        print(e)
        print('error')
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
                      
    except KeyboardInterrupt:
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(23,GPIO.IN)
		GPIO.cleanup()
                update = False
