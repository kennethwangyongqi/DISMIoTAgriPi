from flask import Flask, render_template, jsonify, request,Response
import sys
import json
import numpy
import datetime
from decimal import Decimal
import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer

gevent.monkey.patch_all()

def get_data_from_dynamodb(table,deviceid):
  try:
          import boto3
          from boto3.dynamodb.conditions import Key, Attr
          dynamodb = boto3.resource('dynamodb',
          aws_access_key_id="ASIARSCYLZEPGXCPBNQO",
aws_secret_access_key="43F0Bav/79lgLF5HKZXq+qG7MzyNCyrp/PFAX08Y",
aws_session_token="FQoGZXIvYXdzEAAaDFB7HJbW7C5xok9VfyLxBDmD7wtYLcqSZMS6nqK8g2rgUt6eSsMkXGa09rHWrSz0ohR7NiVyZC84qvgDoTIp7lQk0fVlPWzmPfA8biepLCeKGCXu+YPuQonEG2ThMPaTAYqNykKqHabMsZFhLIXzakoj27U5Xe68G42gEe4M+3U75H5YkEM67r/sHdES9t0NA/fFIVfCq5xihAYexSghuzSE59gfVPb7XL2TI3XA1sSHJ1KX5lM2bLqy4MxdniwuGa5LJ8SAl5NQNV64KzXpLhYxlc5QELcpjm9tmsAL/zbufLzxCl84UDCK0kVWQGqq8cgVWGKPQ7W23vS5ym9USpJSW0y9WaPvB+e4kz6LZPE5gZ338I6sBocVsU7pseUQJ74RWzkOMkMOunWSp/dWQfiY8X8E0yMr7ChPcCH5NLT8aj3nD/C3zBrtyhzwMja0XDyP9eZKKoorS7+k91nTCzCUSEkp79InRhXB/TxOtOO4jCygS5fBLxyU0xRN/3nblD0c7vq56swy1uLEbar2lHuSTuAx7gQvTFH/SZ2ojeCwdmGZ5NqQjk9/CiUCiw10JAB6zrNrBWckX7+zjz0YVFyM7LDW8SKU3aWZidnsJ0zZ6pUBxSg0AzOK3LRCrZ0msoPrfK+za33wBHA1tt7kaD4f7lYT0zeNJDxp5aucrnAXJuU19TQzwzk7lDza1XMmgSNeMQYTN83NXoIhIjgvXp+dHIqc8c11A5nmCFvPrXOvCs+vTJdrYKJHh35FpWs5iq+6neXdmliFRGV+wZ7i5oztwaTWcF4KkMp9wIPzwm5Sf8sq9tVpx/0bbnXnpJqyUl69Zj01oQ1Sh0x1HpvVgbEonYjp6gU=",region_name='us-east-1')
          table = dynamodb.Table(table)
          response = table.query(
              KeyConditionExpression=Key('deviceid').eq(deviceid),
              ScanIndexForward=False
          )
          items = response['Items']
          n=10 # limit to last 10 items
          data = items[:n]
          data_reversed = data[::-1]
          return data_reversed

  except:
      print(sys.exc_info()[0])
      print(sys.exc_info()[1])

class GenericEncoder(json.JSONEncoder):
  def default(self, obj):  
      if isinstance(obj, numpy.generic):
          return numpy.asscalar(obj)
      elif isinstance(obj, Decimal):
          return str(obj) 
      elif isinstance(obj, datetime.datetime):  
          return obj.strftime('%Y-%m-%d %H:%M:%S') 
      elif isinstance(obj, Decimal):
          return float(obj)
      else:  
          return json.JSONEncoder.default(self, obj) 

def data_to_json(data):
  json_data = json.dumps(data,cls=GenericEncoder)
  #print(json_data)
  return json_data                        

app = Flask(__name__)

@app.route("/api/getenvironmentdata",methods = ['POST'])
def apidata_gettemperaturedata():
    if request.method == 'POST':
        try:
            deviceid = request.form['deviceid']
            table = request.form['table']
            data = {'chart_data': data_to_json(get_data_from_dynamodb(table,deviceid)), 'title': "IOT Data"}
            return jsonify(data)
        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])

@app.route("/api/getaccessdata",methods = ['POST'])
def apidata_getaccessdata():
    if request.method == 'POST':
        try:
            deviceid = request.form['deviceid']
            table = request.form['table']
            data = {'access_data': data_to_json(get_data_from_dynamodb(table,deviceid)), 'title': "IOT Data"}
            return jsonify(data)
        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])

@app.route("/api/getlastestimg",methods = ['POST'])
def apidata_getimgdata():
    if request.method == 'POST':
        try:
            deviceid = request.form['deviceid']
            table = request.form['table']
            data = {'img_data': data_to_json(get_data_from_dynamodb(table,deviceid)), 'title': "IOT Data"}
            return jsonify(data)
        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
			
@app.route("/pump/<status>",methods = ['POST'])
def pump(status):
    if request.method == 'POST':
	try:
	    deviceid = request.form['deviceid']
	    message = {}
	    message['turn'] = status
	    my_rpi.publish("farm/pump/"+deviceid, json.dumps(message), 1)
            return status
   	except:
	    print(sys.exc_info()[0])
	    print(sys.exc_info()[1])

@app.route("/writeLED/<status>",methods = ['POST'])
def writeled(status):
  if request.method == 'POST':
    try:
      deviceid = request.form['deviceid']
      message = {}
      message["status"] = status
      my_rpi.publish("led/status/"+deviceid, json.dumps(message), 1)
      return status
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])

@app.route("/writebuzz/<status>",methods = ['POST'])
def writebuzz(status):
  if request.method == 'POST':
    try:
      deviceid = request.form['deviceid']
      message = {}
      message["status"] = status
      my_rpi.publish("buzz/status/"+deviceid, json.dumps(message), 1)
      return status
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])

@app.route("/PiCamera/takePic",methods = ['POST'])
def takepic():
  if request.method == 'POST':
    try:
      deviceid = request.form['deviceid']
      message = {}
      message["status"] = 'snap'
      my_rpi.publish("cam/status/"+deviceid, json.dumps(message), 1)
      return 'success'
    except:
      print(sys.exc_info()[0])
      print(sys.exc_info()[1])

@app.route("/")
def index():
    return render_template('index.html')   

@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/greenhouse")
def greenhouse():
    return render_template('greenhouse.html')

@app.route("/farm1")
def farm1():
    return render_template('farm1.html')

@app.route("/farm2")
def farm2():
    return render_template('farm2.html')

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
host = "a3f69y8dukmi8a-ats.iot.us-east-1.amazonaws.com"
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"

if __name__ == '__main__':
  my_rpi = AWSIoTMQTTClient("PubSub-AgriPi")
  my_rpi.configureEndpoint(host, 8883)
  my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
  my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
  my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
  my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
  my_rpi.configureMQTTOperationTimeout(5)  # 5 sec
  # Connect and subscribe to AWS IoT
  my_rpi.connect()   
  
  try:
    print('Server waiting for requests')
    http_server = WSGIServer(('0.0.0.0', 80), app)
    http_server.serve_forever()
  except:
    print("Exception")
    print(sys.exc_info()[0])
    print(sys.exc_info()[1])
