from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import boto3
import botocore
from time import sleep
import json
import sys

host = "XXXXXXXXXXXXXXXXXXXXX.us-east-1.amazonaws.com"
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"

my_rpi = AWSIoTMQTTClient("farm1-cam")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(10)  # 5 sec

def takepic():
    from picamera import PiCamera
    camera = PiCamera()
    try:
        sleep(3)
        import datetime as datetime
        now = datetime.datetime.now()
        timestring = now.strftime("%d-%m-%YT%H:%M:%S")
        print ("Taking photo " +timestring)
        full_path = '/home/pi/Desktop/AgriPi/photo_'+timestring+'.jpg'
        filename = 'photo_'+timestring+'.jpg'
        camera.capture(full_path)    
        sleep(3)
        print('done taking photo')
        # Upload a new file
        s3.Object(bucket, filename).put(Body=open(full_path, 'rb'))
        print("File uploaded")
        message = {}
        message["deviceid"] = "farm1"
        message["datetime_value"] = now.strftime("%d/%m/%Y, %H:%M:%S")
        message["img_name"] = filename
        my_rpi.publish("img/ref", json.dumps(message), 1)
        print('filename uploaded')
    except Exception as e: 
        print('error')
        print(e)
    finally:
        print('closing cam')
        camera.close()
        print('cam closed')
    
def CamCallback(client, userdata, message):
    print('reach camcallback')
    data = json.loads(message.payload)
    if data['status'] == 'snap':
        takepic()

my_rpi.connect()
my_rpi.subscribe("cam/status/farm1", 1,CamCallback)
# Create an S3 resource
s3 = boto3.resource('s3',aws_access_key_id="XXXXXXXXXXXXXXXXXX",
aws_secret_access_key="XXXXXXXXXXXXXXXXXXXXXXX",
aws_session_token="XXXXXXXXXXXXXXXXXXXXXXX",region_name='us-east-1')

# Set the filename and bucket name
bucket = 'agripibucket' # replace with your own unique bucket name
exists = True

try:
    s3.meta.client.head_bucket(Bucket=bucket)
except botocore.exceptions.ClientError as e:
    error_code = int(e.response['Error']['Code'])
    if error_code == 404:
        exists = False

if exists == False:
  s3.create_bucket(Bucket=bucket,CreateBucketConfiguration={
    'LocationConstraint': 'us-east-1'})

print('Waits 1 hour before taking another picture...')
loopcount = 0
while True:
    loopcount += 1
    sleep(3600)
    try:
        takepic()
    except Exception as e:
        print('loop error')
        print(e)
