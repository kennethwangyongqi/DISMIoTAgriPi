import sys
import json
from time import sleep
import RPi.GPIO as GPIO
from gpiozero import LED
from gpiozero import Buzzer
import MFRC522
import signal
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

host = "XXXXXXXXXXXXXXXXXX.us-east-1.amazonaws.com"
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"

my_rpi = AWSIoTMQTTClient("greenhouse1-rfid")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec

#control LED through web app
def LedCallback(client, userdata, message):
    print('led')
    data = json.loads(message.payload)
    if data['status'] == 'On':
        greenled.on()
        redled.on()
    elif data['status'] == 'Off':
        greenled.off()
        redled.off()

#control buzzer through web app
def BuzzCallback(client, userdata, message):
    print('buzz')
    data = json.loads(message.payload)
    if data['status'] == 'On':
        bz.on()
    elif data['status'] == 'Off':
        bz.off()
        
   
# Connect and subscribe to AWS IoT
my_rpi.connect()
my_rpi.subscribe("led/status/greenhouse_1", 1, LedCallback)
my_rpi.subscribe("buzz/status/greenhouse_1", 1, BuzzCallback)
uid = None 
continue_reading = True
greenled = LED(20)
redled = LED(21)
bz = Buzzer(26)

    # Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

    # Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

    # Create an object of the class MFRC522
mfrc522 = MFRC522.MFRC522()

    # Welcome message
print ("Welcome to the MFRC522 data read example")
print ("Press Ctrl-C to stop.")

    # This loop keeps checking for chips.
    # If one is near it will get the UID
while continue_reading:
      
        # Scan for cards    
    (status,TagType) = mfrc522.MFRC522_Request(mfrc522.PICC_REQIDL)

        # If a card is found
    if status == mfrc522.MI_OK:
        try:
            # Get the UID of the card
            (status,uid) = mfrc522.MFRC522_Anticoll()
            if len(uid) == 5:
                uid = [str(i) for i in uid] 
                uid = ",".join(uid)
                greenled.on()
                bz.on()
                message = {}
                message["deviceid"] = "greenhouse_1"
                import datetime as datetime
                now = datetime.datetime.now()
                message["datetime_value"] = now.strftime("%d/%m/%Y, %H:%M:%S")
                message["card_uid"] = uid
                import json				
                my_rpi.publish("entry/greenhouse", json.dumps(message), 1)
                print(uid+" Inserted")
                bz.off()
                sleep(3)
                greenled.off()
            else:
                redled.on()
                bz.on()
                print("Card not properly detected. Please try again")
                sleep(3)
                redled.off()
                bz.off()
        except KeyboardInterrupt:
            update = False
        except:
            print("Error while inserting data...")
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
