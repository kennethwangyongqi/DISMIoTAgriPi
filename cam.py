from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import boto3
import botocore
from time import sleep
import json
import sys

host = "a3f69y8dukmi8a-ats.iot.us-east-1.amazonaws.com"
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"

my_rpi = AWSIoTMQTTClient("greenhouse1-cam")
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
        message["deviceid"] = "greenhouse_1"
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
my_rpi.subscribe("cam/status/greenhouse_1", 1,CamCallback)
# Create an S3 resource
s3 = boto3.resource('s3',aws_access_key_id="ASIARSCYLZEPKXP2DIDS",
aws_secret_access_key="l095sJrT3Au8LwcHWEJOCEl58mUPKGTW4s0J0xW1",
aws_session_token="FQoGZXIvYXdzEL///////////wEaDHT/uJH0ZHlRcMxgCSLxBEzg+k2GlS/lx8wgbCSgvSPjXCJEhAvBC9t3yYrDZfyodVrZfVL8yaNDIBm74sj/OCxLe5wMWmgJ1xZL6E9lW1/ONxJDQdusVyYelFuUAiCE7vrWAu5krFGviGAi9o9t43XCLzeb0ARl6xDN3MaI6ZPhuReUnF9lLL5Ufzih1nd+cZteLxzhplBjeBDR3ViFgodmuHFDGomuVA5LzgN3gzNvNvrqBvYkETczciC6dxckrb03PXqzL/Y87el0qMxPprg8FjLzJKZFiZStAfonHnY7tGCSGmY+aiJjofsKpXGz2ARMyUtuEj6GNp8Hlbqb7ncgTMkiKO1gRJAPGr+YPcYbKhmnLH0VGqZwgz5C2K9M/GyOyFnGax0SgcpER4jRSSGPgEs7xub4v0Q4o1KPLsMEKmsAQtxIHMJaFNsYU65ifLzeVPlV+hmCbKY4iMjpF2o6sUA37AhmhMYN6em45bx9nwbJupBKpkdQOMrF8tcwx66cO9GfjeJlLtuBecWipgbATEXNYeLUyruwos1j7fRUdsfPTH7QY1FPgOBexZNbfrrFQ1dR7uUFdm0l/LALcnx0Cpwl0NFJPnoL5oqcs8/fX3q4+o94RJevun7TboVHltD20HxCcWhUQ2ID8IWXsO98VoXX+IXCFgMZCUidmIogYDyWxdToRgUkiqiZ++W9ItO5FiSF1r8Bw000rQbA9W2Cy4iNFVrTK/Lh85cnspidFrBJIBEOFECFV6ZPm7OeeGVwaKEODm7Vb5T6GZ53LeILjYfKdQH6mtFJ81JVQ6EwWMd3TxtIy8amR9bZcWobI+4Lkmy1lQ5poAbEYpVQJwIo0OLa6gU=",region_name='us-east-1')

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

print('Waiting....')
loopcount = 0
while True:
    loopcount += 1
    sleep(30)
    try:
        takepic()
    except Exception as e:
        print('loop error')
        print(e)