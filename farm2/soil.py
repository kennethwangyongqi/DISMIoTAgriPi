#device libraries
import sys
import Adafruit_DHT
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
host = "xxxxxxxxxxxxxxxxx.us-east-1.amazonaws.com"
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"

#mqtt connection
my_rpi = AWSIoTMQTTClient("farm2-irrigation")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec

def checking():
    try:
        publisher()
        lcd.text('Soil is dry',1)
        lcd.text('SNS alert sent',2)
        print("Soil moisture is dry... ")
        print("Sending SNS alert...") 
        sleep(1)
        print("SNS alert sent")
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
        message["deviceid"] = "farm2"
        now = datetime.datetime.now()
        message["datetime_value"] = now.strftime("%d/%m/%Y, %H:%M:%S")
        message["alert"] = 1		
        my_rpi.publish("farm/pump", json.dumps(message), 1)
    except Exception as e: 
        print(e)
        print('error')
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
            
my_rpi.connect()
print("Successfully connected to MQTT!")

update = True
while update:
    try:
        lcd = LCD()
        if soil.is_held:
            lcd.text('Soil is wet',1)
            print("Soil moisture is wet")
            sleep(10)

        else:
            print("Checking Soil moisture after 10 seconds...")
            sleep(5)
            checking()
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
