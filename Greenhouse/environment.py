import sys
import Adafruit_DHT
from time import sleep
from rpi_lcd import LCD
from gpiozero import MCP3008
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

pin = 4
lcd = LCD()
update = True
mcp3008 = MCP3008(channel=0)

host = "a3f69y8dukmi8a-ats.iot.us-east-1.amazonaws.com"
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"

my_rpi = AWSIoTMQTTClient("greenhouse1-environment")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec
my_rpi.connect()

#main
try:
    while update:
        try:
            #get humidity, temperature and light values
            humidity, temperature = Adafruit_DHT.read_retry(11, pin)
            light = (1024*(1.0-mcp3008.value))
            light = round(light)

            #setting values as json format to publish to dynamoDB
            message = {}
            message["deviceid"] = "greenhouse_1"
            import datetime as datetime
            now = datetime.datetime.now()
            message["datetime_value"] = now.strftime("%d/%m/%Y, %H:%M:%S")
            message["temperature_value"] = temperature
            message["humidity_value"] = humidity
            message["light_value"] = light
            import json				
            my_rpi.publish("sensors/environment/greenhouse", json.dumps(message), 1)
            print("Wait 4 secs before getting next temperature and humidity values..")
            sleep(2)

            #display temperature and humidity on LCD
            lcd.text("Temp: "+ str(temperature) + unichr(223) + "C", 1)
            lcd.text("Humidity: "+ str(humidity)+"%", 2)
        except KeyboardInterrupt:
            update=False
            lcd.clear()
        except:
            print("Error while inserting data...")
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
except:
    print(sys.exc_info()[0])
    print(sys.exc_info()[1])
