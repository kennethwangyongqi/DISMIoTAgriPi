###### ST0324 Internet of Things CA2 Step-by-step Tutorial

###### SCHOOL OF COMPUTING (SOC)

# IOT CA2 AgriPi

## Table of Contents

- Section 1 Overview of AgriPi
- Section 2 Hardware requirements
- Section 3 Hardware setup
- Section 4 Software requirements
- Section 5 Register "AgriPi" as a Thing
- Section 6 Create a S3 Bucket
- Section 7 DynamoDB setup
- Section 8 Create SNS
- Section 9 Hosting of Web Application with AWS EC2
- Section 10 Expected outcome
- Section 11 References

## Section 1 Overview of AgriPi

### What is AgriPi about?
AgriPi is a smart agriculture/automated watering plant system, targetted at home owners who may be overseas on a trip but are unable to attend to their crop. The app has several functions to help monitor and perform actions to control the application from a remote location, such as turning on/off the lighting in the event of low light value, updating the status of the crop by having the Raspberry PI camera to take a picture at that state on demand. 

The next target audience are crop farmers. It will be an added beneficial for the farmers as they are tending to a crop, but not to the massive other plot of crops in the big landscape. Thus, this IoT web app could allow them to monitor the overall temperature and humidity of the environment and if there is a need to, a buzzer can be switched on or off to inform the farmer that a specific crop may require it’s attention. The temperature and humidity will also be displayed on a LCD screen and updated constantly to provide the latest values on ground, an added value to provide them while they are not accessing the web app via the internet.

### How does the final RPI set-up looks like?

### How does the web application look like?

## Section 2 Hardware requirements

### Hardware checklist
#### Three DHT11 Temperature and Humidity Sensors
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img1-DHT11.jpg)

The DHT11 is a low cost digital temperature & humidity sensor that is capable of sensing the surrounding atmosphere using a capacitive humidity sensor and a thermistor. The reading will be signaled out onto the data pin and is fairly simple to use. We will be using one DHT11 sensor on each of the Raspberry Pi as each of the breadboard will be located on a different location. The DHT11 has be added with a 10k ohms resistor to supress the power, or else it will spoil the sensor.

There are 4 pins located on the DHT11:

-	VCC – connect it to 3v3 power
-	DATA – connect it to the GPIO value
-	NC – Stands for No Connection
-	GND – connect it to the ground

The fritzing diagram for setup will be the same for the other DHT11 and should look like this:


#### Two LED 5mm Lights

There will be two different LED lights used to indicate for the RFID sensor entry. Green is for access granted and red is for access denied. 

There are just 2 pins located on the LED::
-	Connect the longer leg pin with blue jumper wire to the GPIO value
-	Connect the shorter leg pin to a 330 ohms resistor and to GND port with black jumper wire

The fritzing diagram setup should look like this for the greenhouse Raspberry Pi:

#### One RFID/ NFC MFRC522 Card Reader Module

We will be using RFID card/tags with a RFID/NFC MFRC522 card reader module that is attached to the greenhouse Raspberry Pi to track, identify and manage access control.

There are 9 pins located on the MFRC522 card reader module and we will only be using 7 of them:

| MFRCF522 pin |	Connect |	RPi pin |	Jumper color |
| :-------: | :------: | :-----: | :--------: |
SDA |	> |	CE0 |	Orange
SCK |	> |	SCLK |	Orange
MOSI |	> |	MOSI |	Purple
MISO |	> |	MISO |	Purple
IDR | | |			
GND |	> |	GND |	Black
RST |	> |	GPIO25 |	Blue
3.3V |	> |	3.3V |	Red
5V |			

The fritzing diagram setup should look like this:

#### Three Light Sensors, with MCP3008 ADC and 10k ohms resistor

Light-Dependant Resistor (LDR) are light sensitive resistors that changes its’ resistance based on how much light they are being exposed to. The more light the LDR receives, the less resistant it becomes. Whereas the darker it becomes, the more resistant it wil be. Since the LDR sensor is an analogue sensor, we will need to supplement it with MCP3008 Analogue Digital Converter to read analogue inputs and convert them into digital signals to the Raspberry Pi. We will need to moderate the flow current by adding a 10k ohms resistor to the LDR sensor.

For the pin number, we will read from left to right on the MCP3008:

|MCP3008 | Raspberry Pi |	Jumper Color |
| :------: | :---------: | :--------: |
| <p>Pin 1<br>VDD</p> | 3V3	| Orange |
| <p>Pin 2<br>VREF</p> | 3V3	| Orange |
| <p>Pin 3<br>AGND</p> | GND	| Grey |
| <p>Pin 4<br>CLK</p> | <p>BCM11<br>SCLK</p>| Yellow |
| <p>Pin 5<br>DOUT</p> | <p>BCM9<br>MISO</p>	| Blue |
| <p>Pin 6<br>DIN</p> | <p>BCM10<br>MOSI</p>	| Pink |
| <p>Pin 7<br>CS/SHDN</p> | <p>BCM18<br>CE0</p>	| Green |
| <p>Pin 8<br>DGND</p> | GND	| Black |
| <p>Pin 1 (Opposite side)</p> | To LDR	| White |

The fritzing diagram setup should look like this:


#### Two Soil Moisture Sensors

The soil moisture sensor is able to detect the amount of moisture present in the soil of the potted plant/farm. It is a low tech sensor that is ideal for monitoring the water level.

We will be connecting a total of 5 jumper wires from the soil sensor to the MH-Sensor-Series Flying-Fish and to the Raspberry Pi.

| Moisture Sensor |	Connect | Flying Fish | Connect |	RPi pin |	Jumper color |
| :-------: | :------: | :-----: | :--------: | :------: | :---------: |
| Any pin | > | + | | | Black |
| Any pin | > | - | | | White |
| | | VCG | > | 5.0v | Purple |
| | | GND | > | GND | Grey |
| | | DO | > | GPIO#23 | Blue |

The fritzing diagram for setup should look like this:

#### Three Buzzers

We will be using active buzzers as they are cheaper and simpler to use. The buzzer is used as an actuator to create alerts by making a buzzing or beeping noise. Resistors is not needed for the buzzer.

There are only 2 pins located on the active buzzer:
-	VOUT 
-	GND

Connect the buzzer to the Raspberry Pi as followed:

| PIR pin | RPi pin |	Jumper Color |
| :------: | :---------: | :--------: |
| GND | GND | Black |
| VOUT | GPIO26 | Blue |

The fritzing diagram setup should look like this:

#### Three RPi PiCamera

The Pi Camera is mounted on and connects through a ribbon cable to the Raspberry Pi. We will be using the Pi Camera to capture images on the greenhouse as well as the farms. 

For the greenhouse RPi, the PiCamera is utilized to see who is at the doorstep when accessing the RFID door.

For the farm 1 and 2 RPi, the PiCamera is utilized and positioned to capture photos of the potted plant/farm.


#### Three LCD Screen
We will be using three 16x2 i2c LCD Screens for each Raspberry Pi. The LCD Screens will be used to dictate data readings on the physical screen:

-	Greenhouse – Temperature & Humidity
-	Farm 1 – Soil moisture & water pump activation
-	Farm 2 – Soil moisture & AWS SNS alerts

Connect both pins on the lcd and the RPi as followed: 


| LCD Pin | RPi Pin |	Jumper Color |
| :------: | :---------: | :--------: |
| SCL | SCL | White |
| SDA | SDA | Yellow |
| GND | GND | Black |
| VCC | 5V | Red |

The final fritzing diagram setup should look like this:

#### 5v 1-Channel Relay Module

We will be using a 1-Channel Relay Module to control a circuit by a separate low-power signal. A relay is an electrically operated switch and uses an electromagnet to mechanically operate a switch.

It has 3 pins for connecting power and for controlling the relay:

-	GND – Connect to GND on the breadboard
-	COM – Connect to GPIO#23
-	VCC – Connect to 5v0 on the breadboard

#### Submersible Water Pump with Tube

This is a low cost, small size Submersible Water Pump Motor which can be operated from a 2.5 ~ 6V power supply. It can take up to 120 liters per hour with very low power consumption. We will connect the piping tube to the motor outlet and submerge it in water. Do take note that dry run may damage the motor due to heating and it will also produce unwanted noise.

*Make sure that the water level is always higher than the motor.* 

The fritzing diagram setup should look like this:

## Section 3 Hardware setup

| Greenhouse RPi | Farm1 RPi | Farm2 RPi |
| :----: | :----: | :----: |
| <p>LCD Screen<br>DHT11 Sensor<br>Light Sensor w/MCP3008 ADC<br>RPi PiCamera<br>Buzzer<br>RFID Sensor<br>RFID cards<br>Green LED<br>Red LED</p> | <p>LCD Screen<br>DHT11 Sensor<br>Light Sensor w/MCP3008 ADC<br>RPi PiCamera<br>Buzzer<br>Soil Moisture Sensor<br>5v Relay Module<br>Submersible Water Pump</p> | <p>LCD Screen<br>DHT11 Sensor<br>Light Sensor w/MCP3008 ADC<br>RPi PiCamera<br>Buzzer<br>Soil Moisture Sensor</p>

#### RPI set-up for Greenhouse RPi

#### RPI set-up for Farm1 RPi

#### RPI set-up for Farm2 RPi

#### Fritzing diagram for Greenhouse RPi

#### Fritzing diagram for Farm1 RPi

#### Fritzing diagram for Farm2 RPi

#### Materials used to set up Greenhouse
We will be using a couple of low cost materials to build our greenhouse set up. Some of our building materials include:

-	Pots for the plants
-	Plants of choice
-	60cm x 40cm styrofoam board to be cut as the walls
-	30cm x 30cm grass patch
-	Styrofoam cubes to hold the plant in place
-	Felt to decorate the walls
-	Soil or something to fill potted plants with

#### Greenhouse Setup

## Section 4 Software requirements
Below is a list of libraries that will be imported and used for each of the python script:

<table>
  <thead>
    <tr>
      <th colspan="3"> Greenhouse Raspberry Pi </th>
    <tr>
      <th>environment.py</th>
      <th>rfid.py</th>
      <th>cam.py</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>sys<br>AWSIoTPythonSDK.MQTTLib, Import AWSIoTMQTTClient<br>time import sleep<br>rpi_lcd import LCD<br>gpiozero import MCP3008, Buzzer<br>Adafruit_DHT<br>RPi.GPIO as GPIO</td>
      <td>sys<br>AWSIoTPythonSDK.MQTTLib, Import AWSIoTMQTTClient<br>time import sleep<br>gpiozero import LED, Buzzer<br>MFRC522<br>Signal<br>json</td>
      <td>sys<br>AWSIoTPythonSDK.MQTTLib, Import AWSIoTMQTTClient<br>time import sleep<br>boto3<br>botocore<br>json<br>json<br>PiCamera<br>datetime</td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr>
      <th colspan="3"> Farm 1 Raspberry Pi </th>
    <tr>
      <th>environment.py</th>
      <th>pump.py</th>
      <th>cam.py</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>sys<br>AWSIoTPythonSDK.MQTTLib, Import AWSIoTMQTTClient<br>time import sleep<br>rpi_lcd import LCD<br>gpiozero import MCP3008, Buzzer<br>Adafruit_DHT<br>RPi.GPIO as GPIO</td>
      <td>sys<br>AWSIoTPythonSDK.MQTTLib, Import AWSIoTMQTTClient<br>time import sleep<br>RPi.GPIO as GPIO<br>datetime as datetime<br>rpi_lcd import LCD<br>json</td>
      <td>sys<br>AWSIoTPythonSDK.MQTTLib, Import AWSIoTMQTTClient<br>time import sleep<br>boto3<br>botocore<br>json<br>json<br>PiCamera<br>datetime</td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr>
      <th colspan="3"> Farm 2 Raspberry Pi </th>
    <tr>
      <th>environment.py</th>
      <th>rfid.py</th>
      <th>cam.py</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>sys<br>AWSIoTPythonSDK.MQTTLib, Import AWSIoTMQTTClient<br>time import sleep<br>rpi_lcd import LCD<br>gpiozero import MCP3008, Buzzer<br>Adafruit_DHT<br>RPi.GPIO as GPIO</td>
      <td>sys<br>AWSIoTPythonSDK.MQTTLib, Import AWSIoTMQTTClient<br>time import sleep<br>RPi.GPIO as GPIO<br>datetime as datetime<br>rpi_lcd import LCD<br>json</td>
      <td>sys<br>AWSIoTPythonSDK.MQTTLib, Import AWSIoTMQTTClient<br>time import sleep<br>boto3<br>botocore<br>json<br>json<br>PiCamera<br>datetime</td>
    </tr>
  </tbody>
</table>


## Section 5 Register "AgriPi" as a Thing

### Set up “AgriPi” as a Thing

1\) Navigate to the AWS console and on the top left panel, click on the Services dropdown to open up the search function. Search for the “IoT Core” service.


2\) On the left navigation panel, Click on Manage > Things. Next, Click on the “Register a Thing” button to start setting up a “Thing”.
 

3\) Click on create a single thing to start setting a “Thing”.

 
4\) Give the device a name, For this we will name it “AgriPi”. Leave the rest of the fields in the creation page as default and click on Next.

 

5\) On the following page, we will generate a X5.09 certificate as well as a public and private key. Choose the “One-click certificate creation (recommended)” option and click on Create certificate. This process will only take 5-10 seconds.

 

6\) The following screen should have a total of Four Downloadable links. It consists of:

-	A certificate
-	A public key
-	A private key
-	A root CA

 

7\) For the root CA, choose the RSA 2048 bit key: Amazon Root CA 1 option. Make sure to right click and select “save link as”. This will enable the download as a .pem file extension.

 

8\) Create a file directory called “cert”, put all 4 newly downloaded files above into this file directory. Rename all of the file with an easier name to indicate the file type:

-	84c3062443-certificate.pem.crt -> certificate.pem.crt
-	84c3062443-public.pem.key -> public.pem.key
-	84c3062443-private.pem.key -> private.pem.key
-	AmazonRootCA1.pem -> rootca.pem

  
The files should be contained in the “cert” directory and look like this.

9\) Next, click on the “Activate”. A Successfully activated certificate notification will appear and the “Activate” button will turn into “Deactivate”.

 

10\) Click on “Done”. After which, the thing will be listed in “Things”.

 

11\) On the left navigation panel, we will proceed to create a secure policy for the AgriPi Thing.
Click on Secure > Policies > Create a policy.

 

12\) Give the new policy a name. For this, we will name it as “AgriPiAllPolicy”.

 

13\) On Action, type in iot* and on Resource ARN, replace it with a *. Ensure that under “Effect”, tick the Allow checkbox. 
Lastly, select “Create”. 

 

14\) A notification will come up saying “ Successfully created a policy”. We will now have a security policy that will allow for access to all IoT Core services.

 
### Attach the AgriPi “Thing” and security policy to the certificate

1\) In this portion, we will begin to attach both the AgriPi and security policy to the X.509 certificate located at the “certificates” navigation panel under Secure. 
Click on the “…” 

 

2\) The following steps below will require to do two things:

-	Select the “AgriPiAllPolicy” to attach the policy
-	Select the “AgriPi” to register the Thing

 

3\) A notification will mention “Successfully attached policy”.
 

4\) Repeat the steps above and select “Attach thing”.

 

5\) A notification will mention “Successfully attached certificate to thing”.

 


### Creating an AWS Role 

In this section,  we will set up a role in order to create rules due to the account being an AWSEducate student type. This account will require extra steps to configure, rather than a paid account which is much more straightforward and does not require more steps. 

1\) Search on the AWS Management Console for “IAM”. Click on the IAM service.

 

2\) On the left navigation panel, the IAM dashboard has a list of features. Click on “Roles”, then click on “Create role”.

 

3\) For the next step, select AWS service and scroll down to select the IOT service.

 
 

4\) Next, after the services we will select the use case. For this instance, select IoT. Click on Next: Permissions to proceed to the next page.

 

5\) In the following page, click on Next: Tags.
 
 

6\) In the following page, click on Next: Review.

 

7\) In the following page, give the role a name. For this instance, we will call it “AgriPiRole”. For the description, leave it as it is by default. Lastly, Click on Create role to finish the step.

 

8\) The following page will have a notification mentioning that the new role “AgriPiRole” has been created. This indicates that the creation is successful.


## Section 6 Create a S3 Bucket

### Create a Bucket

In this section, we will begin to access AWS management console and search for “S3”. The following steps will explain further on the creation.

 

1\) On the S3 Dashboard, click on “Create Bucket”.

 

2\) Type in a unique name for the bucket. For this instance, we shall name it “agripi”. Choose region as “US East (N. Virginia)” which is us-east-1. After this is done, click on “Create” to create a S3 bucket.


 

3\) The newly created bucket should appear at the S3 dashboard.

 



### Editing Public Access Settings and Permissions

1\) In the S3 dashboard, select the newly created bucket by clicking on the check box and choose  “Edit public access settings”.

 

2\) Untick the check box for “Block all public access” and ensure that none of the public access are blocked. Once this is done, click on “Save” to save changes.

 

3\) Type “confirm” in the text field when prompted for a confirmation and click on “Confirm”.

 

4\) From the S3 dashboard, click on the “agripi” bucket then click on the “Permissions” tab on the following page.

 

 

5\) Under the “Permissions” tab, select “Bucket Policy” which will display a text area below.

 

6\) In the text area for Bucket Policy, enter the following policy as shown below:

```
{
    "Version": "2008-10-17",<br>
    "Statement": [
        {
            "Sid": "AllowPublicRead",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::agripi/*"
        }
    ]
}
```
  
7\) When the policy code has been entered, click on “Save”.

 

## Section 7 DynamoDB setup

### Create DynamoDB Tables
In this section, we will begin to access AWS management console and search for “DynamoDB”. The following steps will explain further on the creation.

 

1\) On the DynamoDB Dashboard, click on “Create Table”. Ensure that the Region that the database is configured on is on location as the Thing, else it will not be the same database.

 

2\) Begin creating a table by giving a table name and a primary key. Select add sort key;

-	Table Name = access_log
-	Primary key = deviceid
-	Sort key = datetime_value

 

3\) Click on Create to begin the creation. It will take a few seconds before success.

 

4\) The table will be created and a new table will be registered. 

 

5\) Follow the same steps to create four more tables for:

-	Table name = greenhouse (This database table is for greenhouse environment sensors)
-	Table name = farm (This database table is for farm environment sensors)
-	Table name = pump (This database table is for pump activation)
-	Table name = imgref (This database table is for picam)

 

 

 

 

6\) Verify that all five database tables have been created.

 



### Create AWS IoT Rules

In this section, we will begin by creating an AWS IoT Rule to take information from an incoming MQT message payload and channel the data automatically into the AWS NoSQL DynamoDB database.

1\) Navigate to IoT Core >Act and click on Create to start making a rule.

 

2\) Firstly, we will begin by creating a rule for the greenhouse to retrieve the data from the device:

-	Name -  AccessLogRule
-	Description - Rule to send the data received from greenhouse to the Access_log table

 

3\) Scroll down to Rule query statement. In the query box, type in: 
-	select * FROM ‘entry/greenhouse’

 

4\) Next, click on Add action.
 
 

5\) Select:
-	Split message into multiple Columns of a DynamoDB table (DynamoDBv2)


 

Scroll all the way down and click on “Configure action”.
 

6\) In the Configure action page, there are 4 steps to perform:
-	1. Click on the down button
-	2. Select access_log table
-	3. Select AgriPiRole
-	4. Click on Add action

 

7\) Afterwhich, scroll all the way down and click on Create rule to finish up the rule creation. 
8\) The following screen will show a notification which mentions that the rule has been successfully created. The rule that was created earlier will be shown in the card.

 

9\) The following steps will be a repeat of step 1 – 7 to create the database rule. We will be creating one more rule:
-	EnvironmentRuleForGreenhouse


 
 
 

A separate rule for the farm environment:
-	EnvRuleForFarm

 
 
 

A separate rule for the pump activation:
-	PumpRule

 
 
 

A separate rule for the Image capture:
-	ImgRule

 
 
 

10\) Check and verify that all five rules have been created and enabled.

 

## Section 8 Create SNS

### Create AWS SNS Topic

In this section, we will begin to access AWS management console and search for “SNS” to arricearrive at the AWS SNS dashboard.

 

1\)	Select “Topics” on the side navigation bar.

 

2\)	Click on the “Create new topic” button.

 

3\)	Type in a topic name and a display name for the SNS topic, (Optional), then choose “Create Topic” upon completion. at the botto of the page. In this case we have decided to use “FarmSNS”.
 

4\)	Be sure to take note of the ARN of the newly created SNS topic.

 

### Subscribe to an AWS SNS Topic email notification

In this section, we will show how to send emails whenever IoT data is published.

1\)	Select the newly created SNS topic from the SNS dashboard and click on “Create Subscription”.

 

2\)	On the Create Subscription page, choose Email from the Protocol drop-down list.
Enter in your email address and choose “Create Subscription”.

 

3\)	You will receive a confirmation email saying that the subscription has been sucessfully create. Click on the link provided In the email to continue.

 
 
### Subscribe to mobile SMS notification

To make alerts be published onto a phone for easier viewing, we can create a separate subscription using the SMS protocol and a mobile phone number to receive the notification.

 

Once it is done and you have confirmed both email and SMS to be subscribed, double check that the status shows “Confirmed”.

 


### Create IoT Rule to send alert message

In this section, we will setup alerts sent whenever IoT data is published.

1\)	In the AWS IoT Core dashboard, click the “Act” tab in the sidebar then click on “Create a Rule”.

 

2\)	Enter a name for the rule as well as a description for it in their respective fields.

 

3\)	Type “ select * from ‘farm/pump’ “ into the Rule Query Statement section below:

 

4\)	In the “Set one or more actions” section, click on “Add action”.

 

5\)	Select “Send a message as an SNS push notification” and click on “Configure action”. 

 

6\)	On the configuration page, select the SNS topic created earlier from the “SNS target” drop-down list.

 

7\)	Select the role created previously on section 6 (Creating an AWS Role) and click on “Add Action”, lastly click on “Create Rule”.

 

## Section 9 Hosting of Web Application with AWS EC2
We will use AWS EC2 cloud service to hose the AgriPi as a web application. The following instruction will guide you on how to create, connect, and host the web application on the EC2 instance.

### Create EC2 Instance

1\)	Navigate to the EC2 page with the AWS website by clicking the “Services” tab at the top of the page, then EC2.

 

2\)	Under the “Create Instance” section, click Launch Instance.

 

3\)	Select the Amazon Linux 2 AMI with the 64-bit (x86) option.

 

4\)	Click next with default values until “Step 6: Configure Security Group”. Click “Add Rule” and select HTTP under “Type”. This is to open port 80 and allow for connection to our web interface.

 

5\)	Click “Review and Launch”. At “Step 7: Review Instance Launch”, click “Launch”, and choose create new key pair and enter a key pair name.We will be naming it My_AgriPi_Key. Next, click “Download Key Pair”. This key pair allow us to SSH into the instance later on.

 

6\)	After downloading the key pair, click “Launch Instances”.

 

7\)	At the instance page, you should be able to see the instance created. It will take awhile for the instance to load. 

 

8\)	Once the “Instance State” and “Status Checks” are running and 2/2 respectively, you are ready to connect to the EC2 instance.

 


### Connecting to EC2 Instance

To connect to the EC2 Instance, we will use the third-party program PuTTY. PuTTY will allow us to SSH into the EC2 Instance to execute and perform commands such as running python files. 

To transfer files into the EC2 Instance, we will use the third-party program WinSCP. WinSCP will allow us to transfer the required files for the web application securely. We are using WinSCP also because FileZilla doesn’t work well with EC2 Instance.

1\)	Head over to the following two website to download and install PuTTY and WinSCP.
- PuTTY: https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
- WinSCP: https://winscp.net/eng/download.php

 
 

2\)	Once both software are installed, open PuTTYgen. PuTTYgen allows us to convert the private key format (.pem) generated by Amazon EC2 to the required PuTTY format (.ppk). This is because PuTTY does not support the Amazon EC2’s private key format.

 

3\)	Choose “Load”. To locate your .pem file, select the option “All Files (*.*)” to display files of all types. Select your .pem file for the key pair that u specified when you launched your instance.

 

4\)	After selecting your .pem file, click “Open” and click “OK” on the dialog box.

  
 
5\)	Choose to save private key and click on yes at the warning. Save the file name as My_AgriPi_Key.ppk. 

 

A .ppk file is now saved which means you are ready to SSH into the instance.

 

6\)	In the EC2 Instance management page, take note of the “Public DNS (IPv4)” value. In this case, it is “ec2-54-166-195-124.compute-1.amazonaws.com”. 

 

7\)	For Amazon Linux 2, the default user name is “ec2-user”. Within PuTTY, enter the host name ”ec2-user@ec2-54-166-195-124.compute-1.amazonaws.com”. (user_name@public_dns_name)

8\)	Ensure that the “Connection Type” is SSH and “Port” is 22. 

 

9\)	In the “Category” pane, expand “Connection”, expand “SSH”, and then choose “Auth”. Under “Private key for authentication”, browse to and select the .ppk file you generated previously. 

 

10\)	Click “Open”, then click “Yes” on the PuTTY security alert. 

 

11\)	You should now be SSH in to the EC2 instance.

 

12\)	Now open WinSCP. At the WinSCP login screen, for “Host name”, enter the public DNS hostname or public IPv4 address of your instance. For “User name”, enter the default user name “ec2-user”. Next, click “Advanced”.

 

13\)	In “Advanced”, click “Authentication” under SSH. Under “Private key file”, browse to and select the .ppk file u generated previously. Click “Ok” to return to the login window.

 

14\)	In the login window, click “Save” to save the session as a site. You should see the session save as a site. Once saved, click “Login”.  Click YES when the warning dialog pops up.

 
 

15\)	You are now connected to the instance.

 

15\)	Create a new directory named “ArgiPi” in the instance. 

 



16\)	Navigate into the directory and move the necessary web application and the zip files for the code. Import the rootca.pem, public.pem.key, private.pem.key and certifcate.pem.crt downloaded previously into it.

 

### Running the Web Application

1\)	Open the PuTTY connection that was established earlier and install python-pip. Python-pip will allow us to install the required libraries for python files. Type ‘y’ when asked to.

Sudo yum install python-pip

 

2\)	Install the required libraries for python files.
```
sudo pip install gevent
sudo pip install flask
sudo pip install AWSIoTPythonSDK
sudo pip install boto3
sudo pip install botocore
sudo pip install numpy
```


3\)	Navigate to AgriPi folder and run the server.py file.
```
cd ArgiPi/
sudo python server.py
```
4\)	The web application will now be running live and hosted on AWS EC2. Navigate to the IP address indicated in EC2 instance to launch the web application interface.

## Section 10 Expected outcome

## Section 11 References

2\. Basic Recipes — Gpiozero 1.5.1 Documentation. 2019. 2. Basic Recipes — Gpiozero 1.5.1 Documentation. [ONLINE] Available at: https://gpiozero.readthedocs.io/en/stable/recipes.html. [Accessed 17 August 2019].

14\. API - Output Devices — Gpiozero 1.5.1 Documentation. 2019. 14. API - Output Devices — Gpiozero 1.5.1 Documentation. [ONLINE] Available at: https://gpiozero.readthedocs.io/en/stable/api_output.html. [Accessed 17 August 2019].

Circuit Basics. 2019. How to Setup an LCD on the Raspberry Pi and Program It With Python - Circuit Basics. [ONLINE] Available at: http://www.circuitbasics.com/raspberry-pi-lcd-set-up-and-programming-in-python/. [Accessed 17 August 2019].

Gist. 2019. A template to make good README.md · GitHub. [ONLINE] Available at: https://gist.github.com/PurpleBooth/109311bb0361f32d87a2. [Accessed 17 August 2019].

Gist. 2019. water.py · GitHub. [ONLINE] Available at: https://gist.github.com/benrules2/6f490f3a0e082ae6592a630bd7abe588. [Accessed 17 August 2019].

Raspberry Pi Water Pump Python Code | CodeDigs. 2019. Raspberry Pi Water Pump Python Code | CodeDigs. [ONLINE] Available at: https://codedigs.com/raspberry-pi-water-pump-python-code/. [Accessed 17 August 2019].

Water pump connected to relay keeps on running - Raspberry Pi Forums. 2019. Water pump connected to relay keeps on running - Raspberry Pi Forums. [ONLINE] Available at: https://www.raspberrypi.org/forums/viewtopic.php?t=207797. [Accessed 17 August 2019].

www.instructables.com. 2019. No page title. [ONLINE] Available at: https://www.instructables.com/id/Raspberry-Pi-Controlled-Irrigation-System/. [Accessed 17 August 2019].

YouTube. 2019. 5 Volt Relay (Raspberry Pi) - YouTube. [ONLINE] Available at: https://www.youtube.com/watch?v=51f3ZazNW-w&t=1s. [Accessed 17 August 2019].

YouTube. 2019. How to build an easy automatic watering system for seedlings using a Raspberry pi - YouTube. [ONLINE] Available at: https://www.youtube.com/watch?v=AsGe-sQkMI0. [Accessed 17 August 2019].

YouTube. 2019. Soil Moisture Sensor (Raspberry Pi) - YouTube. [ONLINE] Available at: https://www.youtube.com/watch?v=9LxrX5Eeukg&t=1s. [Accessed 17 August 2019].
```
-- End of CA2 Step-by-step tutorial --
```
