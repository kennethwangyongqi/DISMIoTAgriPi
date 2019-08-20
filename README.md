###### ST0324 Internet of Things CA2 Step-by-step Tutorial

###### SCHOOL OF COMPUTING (SOC)

# IOT CA2 AgriPi

## Table of Contents

- Section 1 Overview of AgriPi
- Section 2 Hardware requirements
- Section 3 Hardware setup
- Section 4 Software requirements
- Section 5 Software setup requirements
- Section 6 Register "AgriPi" as a Thing
- Section 7 Create a S3 Bucket
- Section 8 DynamoDB setup
- Section 9 Create SNS
- Section 10 Hosting of Web Application with AWS EC2
- Section 11 Expected outcome
- Section 12 References

## Section 1 Overview of AgriPi

### What is AgriPi about?
The description of our application is that it is a smart agriculture/automated watering plant system, targetted at home owners who may be overseas on a trip but are unable to attend to their crop. The app has several functions to help monitor and perform actions to control the application from a remote location, such as turning on/off the lighting in the event of low light value, updating the status of the crop by having the Raspberry Pi camera to take a picture at that state on demand and more. 

The next target audience are crop farmers. It will be an added beneficial for the farmers as they are tending to a crop. This IoT project could allow them to monitor the overall temperature and humidity of the environment, control actuator like the water pump. If there is a need to, a buzzer can be switched on or off to inform the farmer that a specific crop may require it’s attention. The temperature and humidity will also be displayed on a LCD screen and updated constantly to provide the latest values on ground, an added value to provide them while they are not accessing the web app via the internet. The soil moisture will also be displayed on the LCD screen for the farm raspberry Pi to indicate if it is wet or dry. Values will also be sent via the cloud service to the DynamoDB database to keep a record of all the data sent using the Raspberry Pi. 

We believe that this Agriculture IoT project will benefit the target audience and make their life easier by reducing workload and creating a smarter planting environment.


### How does the final RPI set-up looks like?
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img-FinalAgriPiSetup.jpg)

### How does the web application look like?

#### Final web application design

##### AgriPi homepage

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/webappindex.png)

##### Greenhouse dashboard

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/webappgreenhouse.png)

##### Farm 1 dashboard

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/webappfarm1.png)

##### Farm 2 dashboard
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/webappfarm2.png)

#### System Architecture

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/sysarch.png)

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

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img2-DHT11Fritz.jpg)

#### Two LED 5mm Lights

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img3-greenLED.jpg)
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img4-redLED.jpg)

There will be two different LED lights used to indicate for the RFID sensor entry. Green is for access granted and red is for access denied. 

There are just 2 pins located on the LED::
-	Connect the longer leg pin with blue jumper wire to the GPIO value
-	Connect the shorter leg pin to a 330 ohms resistor and to GND port with black jumper wire

The fritzing diagram setup should look like this for the greenhouse Raspberry Pi:

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img5-LEDfritz.jpg)

#### One RFID/ NFC MFRC522 Card Reader Module

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img6-RFIDsensor.jpg)
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img7-RFIDcard.jpg)

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

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img8-RFIDfritz.jpg)

#### Three Light Sensors, with MCP3008 ADC and 10k ohms resistor

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img9-LDRsensor.jpg)
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img10-mcp3008.jpg)
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img11-LDRresistor.jpg)

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

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img12-LDRfritz.jpg)


#### Two Soil Moisture Sensors

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img13-Soilsensor.jpg)

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

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img14-Soilfritz.jpg)

#### Three Buzzers

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img15-Buzzer.jpg)

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

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img16-Buzzerfritz.jpg)

#### Three RPi PiCamera

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img17-piCam.jpg)

The Pi Camera is mounted on and connects through a ribbon cable to the Raspberry Pi. We will be using the Pi Camera to capture images on the greenhouse as well as the farms. 

For the greenhouse RPi, the PiCamera is utilized to see who is at the doorstep when accessing the RFID door.

For the farm 1 and 2 RPi, the PiCamera is utilized and positioned to capture photos of the potted plant/farm.


#### Three LCD Screen

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img18-LCD.jpg)

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

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img19-LCDfritz.jpg)

#### 5v 1-Channel Relay Module

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img20-Relay1.jpg)
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img21-Relay2.jpg)


We will be using a 1-Channel Relay Module to control a circuit by a separate low-power signal. A relay is an electrically operated switch and uses an electromagnet to mechanically operate a switch.

It has 3 pins for connecting power and for controlling the relay:

-	GND – Connect to GND on the breadboard
-	COM – Connect to GPIO#23
-	VCC – Connect to 5v0 on the breadboard

#### Submersible Water Pump with Tube

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img22-WaterPump.jpg)

This is a low cost, small size Submersible Water Pump Motor which can be operated from a 2.5 ~ 6V power supply. It can take up to 120 liters per hour with very low power consumption. We will connect the piping tube to the motor outlet and submerge it in water. Do take note that dry run may damage the motor due to heating and it will also produce unwanted noise.

*Make sure that the water level is always higher than the motor.* 

The fritzing diagram setup should look like this:

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img23-WaterPumpfritz.jpg)

## Section 3 Hardware setup

| Greenhouse RPi | Farm1 RPi | Farm2 RPi |
| :----: | :----: | :----: |
| <p>LCD Screen<br>DHT11 Sensor<br>Light Sensor w/MCP3008 ADC<br>RPi PiCamera<br>Buzzer<br>RFID Sensor<br>RFID cards<br>Green LED<br>Red LED</p> | <p>LCD Screen<br>DHT11 Sensor<br>Light Sensor w/MCP3008 ADC<br>RPi PiCamera<br>Buzzer<br>Soil Moisture Sensor<br>5v Relay Module<br>Submersible Water Pump</p> | <p>LCD Screen<br>DHT11 Sensor<br>Light Sensor w/MCP3008 ADC<br>RPi PiCamera<br>Buzzer<br>Soil Moisture Sensor</p>

#### RPI set-up for Greenhouse RPi

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img24-GreenhouseSetup.jpg)

#### RPI set-up for Farm1 RPi

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img25-Farm1Setup.jpg)

#### RPI set-up for Farm2 RPi

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img26-Farm2Setup.jpg)

#### Fritzing diagram for Greenhouse RPi

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img27-Greenhousefritz.jpg)

#### Fritzing diagram for Farm1 RPi

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img28-Farm1fritz.jpg)

#### Fritzing diagram for Farm2 RPi

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img29-Farm2fritz.jpg)

#### Materials used to set up Greenhouse

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/img30hardwaresetup.jpg)

We will be using a couple of low cost materials to build our greenhouse set up. Some of our building materials include:

-	Pots for the plants
-	Plants of choice
-	60cm x 40cm styrofoam board to be cut as the walls
-	30cm x 30cm grass patch
-	Styrofoam cubes to hold the plant in place
-	Felt to decorate the walls
-	Soil or something to fill potted plants with

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

## Section 5 Software setup requirements
 
1\) To deploy the web application, the Flask and gevent libraries need to be installed on the EC2 instance. With reference to IOT practical 3, section 6, install the libraries using the commands below:

Install Flask (http://flask.pocoo.org/)
``` sudo pip install flask ```
Install gevent (http://www.gevent.org)
``` sudo pip install gevent ```

2\) To implement the Pi Camera, the camera has to be enabled inside the raspberry pi configuration. With reference to IOT practical 4, section 6:

  - Open the Raspberry Pi Configuration Tool from the main menu:
  
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup1.jpg)

  - Ensure the camera software is enabled. If it's not enabled, enable it and reboot the RPi to begin.
  
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup2.jpg)

  - To implement the LCD screen, the rpi_lcd library need to be installed. With reference to IOT practical 4 additional, section 4, install the rpi_lcd library using the command below:
  ``` sudo pip install rpi-lcd ```


  - To implement RFID, there are configuration and libraries to be added. With reference to IOT practical 5 additional, section 4, if you are using  the ST0324 IoT Raspbian image, the following configuration have already been done and you do not need to do this step. However, if you are using a fresh image, you would need to the following steps.
  ``` sudo rasp-config ```
  
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup3.jpg)


![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup4.jpg)

\<\< Enable device tree in boot.txt\>\>
Modify the /boot/config.txt to enable SPI.

``` sudo nano /boot/config.txt ```

Ensure these lines are included in config.txt.

``` device_tree_param=spi=on
dtoverlay=spi-bcm2835 
```

\<\< Install Python-dev \>\>
Make sure there is an active Internet connection as the follow commands require Internet access.
Install the Python development libraries.
``` sudo apt-get install python-dev ```

\<\< Install SPI-Py Library \>\>
Set up the SPI Python libraries since the card reader uses the SPI interface.
``` cd ~
git clone https://github.com/lthiery/SPI-Py.git
cd ~/SPI-Py
sudo python setup.py install 
```

 
Install the AWS Command-Line Interface Client, if it is installed and not updated, add “- -“update at the end of the command.
 ``` sudo pip install awscli --update ```
 
 Access the AWS Educate Account, Sign in and click on “Account Details” to get the AWS credentials.
 
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup5.jpg)

Click on the Show button and copy the AWS CLI code that is shown onto a notepad.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup6.jpg)

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup7.jpg)

Back to the RPi, open a new terminal and type in:
``` sudo nano ~/.aws/credentials ```

Paste the previously copied AWS CLI code into the nano editor, overwrite and save.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup8.jpg)


## Section 6 Register "AgriPi" as a Thing

### Set up “AgriPi” as a Thing

1\) Navigate to the AWS console and on the top left panel, click on the Services dropdown to open up the search function. Search for the “IoT Core” service.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup9.jpg)
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup10.jpg)


2\) On the left navigation panel, Click on Manage > Things. Next, Click on the “Register a Thing” button to start setting up a “Thing”.
 
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup11.jpg)

3\) Click on create a single thing to start setting a “Thing”.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup12.jpg)
 
4\) Give the device a name, For this we will name it “AgriPi”. Leave the rest of the fields in the creation page as default and click on Next.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup13.jpg)

5\) On the following page, we will generate a X5.09 certificate as well as a public and private key. Choose the “One-click certificate creation (recommended)” option and click on Create certificate. This process will only take 5-10 seconds.

 ![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup14.jpg)

6\) The following screen should have a total of Four Downloadable links. It consists of:

-	A certificate
-	A public key
-	A private key
-	A root CA

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup15.jpg)

7\) For the root CA, choose the RSA 2048 bit key: Amazon Root CA 1 option. Make sure to right click and select “save link as”. This will enable the download as a .pem file extension.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup16.jpg)

8\) Create a file directory called “cert”, put all 4 newly downloaded files above into this file directory. Rename all of the file with an easier name to indicate the file type:

-	84c3062443-certificate.pem.crt -> certificate.pem.crt
-	84c3062443-public.pem.key -> public.pem.key
-	84c3062443-private.pem.key -> private.pem.key
-	AmazonRootCA1.pem -> rootca.pem

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup17.jpg)

The files should be contained in the “cert” directory and look like this.

9\) Next, click on the “Activate”. A Successfully activated certificate notification will appear and the “Activate” button will turn into “Deactivate”.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup18.jpg)

10\) Click on “Done”. After which, the thing will be listed in “Things”.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup19.jpg)

11\) On the left navigation panel, we will proceed to create a secure policy for the AgriPi Thing.
Click on Secure > Policies > Create a policy.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup20.jpg) 

12\) Give the new policy a name. For this, we will name it as “AgriPiAllPolicy”.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup21.jpg) 

13\) On Action, type in iot* and on Resource ARN, replace it with a *. Ensure that under “Effect”, tick the Allow checkbox. 
Lastly, select “Create”. 

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup22.jpg)

14\) A notification will come up saying “ Successfully created a policy”. We will now have a security policy that will allow for access to all IoT Core services.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup23.jpg)

### Attach the AgriPi “Thing” and security policy to the certificate

1\) In this portion, we will begin to attach both the AgriPi and security policy to the X.509 certificate located at the “certificates” navigation panel under Secure. 
Click on the “…” 

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup24.jpg)

2\) The following steps below will require to do two things:

-	Select the “AgriPiAllPolicy” to attach the policy
-	Select the “AgriPi” to register the Thing

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup25.jpg)
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup26.jpg)

3\) A notification will mention “Successfully attached policy”.
 
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup27.jpg)

4\) Repeat the steps above and select “Attach thing”.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup28.jpg)

5\) A notification will mention “Successfully attached certificate to thing”.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup29.jpg)

### Creating an AWS Role 

In this section,  we will set up a role in order to create rules due to the account being an AWSEducate student type. This account will require extra steps to configure, rather than a paid account which is much more straightforward and does not require more steps. 

1\) Search on the AWS Management Console for “IAM”. Click on the IAM service.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup30.jpg) 

2\) On the left navigation panel, the IAM dashboard has a list of features. Click on “Roles”, then click on “Create role”.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup31.jpg) 

3\) For the next step, select AWS service and scroll down to select the IOT service.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup32.jpg)
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup33.jpg)

4\) Next, after the services we will select the use case. For this instance, select IoT. Click on Next: Permissions to proceed to the next page.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup34.jpg) 

5\) In the following page, click on Next: Tags.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup35.jpg) 

6\) In the following page, click on Next: Review.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup36.jpg) 

7\) In the following page, give the role a name. For this instance, we will call it “AgriPiRole”. For the description, leave it as it is by default. Lastly, Click on Create role to finish the step.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup37.jpg) 

8\) The following page will have a notification mentioning that the new role “AgriPiRole” has been created. This indicates that the creation is successful.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup38.jpg)

## Section 8 Create a S3 Bucket

### Create a Bucket

In this section, we will begin to access AWS management console and search for “S3”. The following steps will explain further on the creation.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup39.jpg) 

1\) On the S3 Dashboard, click on “Create Bucket”.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup40.jpg) 

2\) Type in a unique name for the bucket. For this instance, we shall name it “agripi”. Choose region as “US East (N. Virginia)” which is us-east-1. After this is done, click on “Create” to create a S3 bucket.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup41.jpg)

3\) The newly created bucket should appear at the S3 dashboard.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup42.jpg)

### Editing Public Access Settings and Permissions

1\) In the S3 dashboard, select the newly created bucket by clicking on the check box and choose  “Edit public access settings”.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup43.jpg)

2\) Untick the check box for “Block all public access” and ensure that none of the public access are blocked. Once this is done, click on “Save” to save changes.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup44.jpg) 

3\) Type “confirm” in the text field when prompted for a confirmation and click on “Confirm”.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup45.jpg) 

4\) From the S3 dashboard, click on the “agripi” bucket then click on the “Permissions” tab on the following page.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup46.jpg)
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup47.jpg)

5\) Under the “Permissions” tab, select “Bucket Policy” which will display a text area below.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup48.jpg) 

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

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup49.jpg) 

## Section 8 DynamoDB setup

### Create DynamoDB Tables
In this section, we will begin to access AWS management console and search for “DynamoDB”. The following steps will explain further on the creation.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup50.jpg) 

1\) On the DynamoDB Dashboard, click on “Create Table”. Ensure that the Region that the database is configured on is on location as the Thing, else it will not be the same database.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup51.jpg) 

2\) Begin creating a table by giving a table name and a primary key. Select add sort key;

-	Table Name = access_log
-	Primary key = deviceid
-	Sort key = datetime_value

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup52.jpg) 

3\) Click on Create to begin the creation. It will take a few seconds before success.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup53.jpg) 

4\) The table will be created and a new table will be registered. 

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup54.jpg)

5\) Follow the same steps to create four more tables for:

-	Table name = greenhouse (This database table is for greenhouse environment sensors)
-	Table name = farm (This database table is for farm environment sensors)
-	Table name = pump (This database table is for pump activation)
-	Table name = imgref (This database table is for picam)

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup55.jpg)
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup56.jpg)
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup57.jpg)
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup58.jpg)

6\) Verify that all five database tables have been created.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup59.jpg)

### Create AWS IoT Rules

In this section, we will begin by creating an AWS IoT Rule to take information from an incoming MQT message payload and channel the data automatically into the AWS NoSQL DynamoDB database.

1\) Navigate to IoT Core >Act and click on Create to start making a rule.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup60.jpg) 

2\) Firstly, we will begin by creating a rule for the greenhouse to retrieve the data from the device:

-	Name -  AccessLogRule
-	Description - Rule to send the data received from greenhouse to the Access_log table

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup61.jpg) 

3\) Scroll down to Rule query statement. In the query box, type in: 
-	select * FROM ‘entry/greenhouse’

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup62.jpg) 

4\) Next, click on Add action.
 
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup63.jpg) 

5\) Select:
-	Split message into multiple Columns of a DynamoDB table (DynamoDBv2)

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup64.jpg)

Scroll all the way down and click on “Configure action”.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup65.jpg)

6\) In the Configure action page, there are 4 steps to perform:
-	1. Click on the down button
-	2. Select access_log table
-	3. Select AgriPiRole
-	4. Click on Add action

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup66.jpg)

7\) Afterwhich, scroll all the way down and click on Create rule to finish up the rule creation.

8\) The following screen will show a notification which mentions that the rule has been successfully created. The rule that was created earlier will be shown in the card.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup67.jpg) 

9\) The following steps will be a repeat of step 1 – 7 to create the database rule. We will be creating one more rule:
-	EnvironmentRuleForGreenhouse

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup68.jpg)
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup69.jpg)
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup70.jpg) 

A separate rule for the farm environment:
-	EnvRuleForFarm

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup71.jpg)
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup72.jpg)
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup73.jpg) 

A separate rule for the pump activation:
-	PumpRule

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup74.jpg)
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup75.jpg)
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup76.jpg)
 
A separate rule for the Image capture:
-	ImgRule

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup77.jpg)
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup78.jpg)
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup79.jpg) 

10\) Check and verify that all five rules have been created and enabled.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup80.jpg) 

## Section 9 Create SNS

### Create AWS SNS Topic

In this section, we will begin to access AWS management console and search for “SNS” to arricearrive at the AWS SNS dashboard.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup81.jpg)  

1\)	Select “Topics” on the side navigation bar.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup82.jpg)  

2\)	Click on the “Create new topic” button.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup83.jpg) 

3\)	Type in a topic name and a display name for the SNS topic, (Optional), then choose “Create Topic” upon completion. at the botto of the page. In this case we have decided to use “FarmSNS”.
 
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup84.jpg) 

4\)	Be sure to take note of the ARN of the newly created SNS topic.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup85.jpg)  

### Subscribe to an AWS SNS Topic email notification

In this section, we will show how to send emails whenever IoT data is published.

1\)	Select the newly created SNS topic from the SNS dashboard and click on “Create Subscription”.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup86.jpg)  

2\)	On the Create Subscription page, choose Email from the Protocol drop-down list.
Enter in your email address and choose “Create Subscription”.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup87.jpg)  

3\)	You will receive a confirmation email saying that the subscription has been sucessfully create. Click on the link provided In the email to continue.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup88.jpg)
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup89.jpg) 
 
### Subscribe to mobile SMS notification

To make alerts be published onto a phone for easier viewing, we can create a separate subscription using the SMS protocol and a mobile phone number to receive the notification.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup90.jpg)  

Once it is done and you have confirmed both email and SMS to be subscribed, double check that the status shows “Confirmed”.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup91.jpg)  

### Create IoT Rule to send alert message

In this section, we will setup alerts sent whenever IoT data is published.

1\)	In the AWS IoT Core dashboard, click the “Act” tab in the sidebar then click on “Create a Rule”.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup92.jpg)  

2\)	Enter a name for the rule as well as a description for it in their respective fields.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup93.jpg)  

3\)	Type “ select * from ‘farm/pump’ “ into the Rule Query Statement section below:

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup94.jpg)  

4\)	In the “Set one or more actions” section, click on “Add action”.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup95.jpg)  

5\)	Select “Send a message as an SNS push notification” and click on “Configure action”. 

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup96.jpg)  

6\)	On the configuration page, select the SNS topic created earlier from the “SNS target” drop-down list.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup97.jpg)  

7\)	Select the role created previously on section 6 (Creating an AWS Role) and click on “Add Action”, lastly click on “Create Rule”.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup98.jpg)  

## Section 10 Hosting of Web Application with AWS EC2
We will use AWS EC2 cloud service to hose the AgriPi as a web application. The following instruction will guide you on how to create, connect, and host the web application on the EC2 instance.

### Create EC2 Instance

1\)	Navigate to the EC2 page with the AWS website by clicking the “Services” tab at the top of the page, then EC2.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup99.jpg)  

2\)	Under the “Create Instance” section, click Launch Instance.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup100.jpg)  

3\)	Select the Amazon Linux 2 AMI with the 64-bit (x86) option.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup101.jpg)  

4\)	Click next with default values until “Step 6: Configure Security Group”. Click “Add Rule” and select HTTP under “Type”. This is to open port 80 and allow for connection to our web interface.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup102.jpg)  

5\)	Click “Review and Launch”. At “Step 7: Review Instance Launch”, click “Launch”, and choose create new key pair and enter a key pair name.We will be naming it My_AgriPi_Key. Next, click “Download Key Pair”. This key pair allow us to SSH into the instance later on.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup103.jpg)  

6\)	After downloading the key pair, click “Launch Instances”.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup104.jpg)  

7\)	At the instance page, you should be able to see the instance created. It will take awhile for the instance to load. 

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup105.jpg)  

8\)	Once the “Instance State” and “Status Checks” are running and 2/2 respectively, you are ready to connect to the EC2 instance.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup106.jpg) 

### Connecting to EC2 Instance

To connect to the EC2 Instance, we will use the third-party program PuTTY. PuTTY will allow us to SSH into the EC2 Instance to execute and perform commands such as running python files. 

To transfer files into the EC2 Instance, we will use the third-party program WinSCP. WinSCP will allow us to transfer the required files for the web application securely. We are using WinSCP also because FileZilla doesn’t work well with EC2 Instance.

1\)	Head over to the following two website to download and install PuTTY and WinSCP.
- PuTTY: https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
- WinSCP: https://winscp.net/eng/download.php

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup107.jpg)
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup108.jpg)  

2\)	Once both software are installed, open PuTTYgen. PuTTYgen allows us to convert the private key format (.pem) generated by Amazon EC2 to the required PuTTY format (.ppk). This is because PuTTY does not support the Amazon EC2’s private key format.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup109.jpg)  

3\)	Choose “Load”. To locate your .pem file, select the option “All Files (*.*)” to display files of all types. Select your .pem file for the key pair that u specified when you launched your instance.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup110.jpg)  

4\)	After selecting your .pem file, click “Open” and click “OK” on the dialog box.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup111.jpg)   
 
5\)	Choose to save private key and click on yes at the warning. Save the file name as My_AgriPi_Key.ppk. 

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup112.jpg)  

A .ppk file is now saved which means you are ready to SSH into the instance.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup113.jpg)  

6\)	In the EC2 Instance management page, take note of the “Public DNS (IPv4)” value. In this case, it is “ec2-54-166-195-124.compute-1.amazonaws.com”. 

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup114.jpg)  

7\)	For Amazon Linux 2, the default user name is “ec2-user”. Within PuTTY, enter the host name ”ec2-user@ec2-54-166-195-124.compute-1.amazonaws.com”. (user_name@public_dns_name)

8\)	Ensure that the “Connection Type” is SSH and “Port” is 22. 

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup115.jpg)  

9\)	In the “Category” pane, expand “Connection”, expand “SSH”, and then choose “Auth”. Under “Private key for authentication”, browse to and select the .ppk file you generated previously. 

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup116.jpg)  

10\)	Click “Open”, then click “Yes” on the PuTTY security alert. 

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup117.jpg)  

11\)	You should now be SSH in to the EC2 instance.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup118.jpg)  

12\)	Now open WinSCP. At the WinSCP login screen, for “Host name”, enter the public DNS hostname or public IPv4 address of your instance. For “User name”, enter the default user name “ec2-user”. Next, click “Advanced”.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup119.jpg)  

13\)	In “Advanced”, click “Authentication” under SSH. Under “Private key file”, browse to and select the .ppk file u generated previously. Click “Ok” to return to the login window.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup120.jpg)  

14\)	In the login window, click “Save” to save the session as a site. You should see the session save as a site. Once saved, click “Login”.  Click YES when the warning dialog pops up.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup121.jpg)  
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup122.jpg)  

15\)	You are now connected to the instance.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup123.jpg)  

16\)	Create a new directory named “ArgiPi” in the instance. 

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup124.jpg)  
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup125.jpg) 


17\)	Navigate into the directory and move the necessary web application and the zip files for the code. Import the rootca.pem, public.pem.key, private.pem.key and certifcate.pem.crt downloaded previously into it.

![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup126.jpg)  

### Running the Web Application

1\)	Open the PuTTY connection that was established earlier and install python-pip. Python-pip will allow us to install the required libraries for python files. Type ‘y’ when asked to.
```
Sudo yum install python-pip
```
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/setup127.jpg)  

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

## Section 11 Expected outcome

To test if the program works, run all the python files. server.py will be run on the AWS EC2 side. The following is the link to the video demonstration of what the application should look like.

### Greenhouse RPi

Firstly, Greenhouse should populate the database with environment data (temperature, humidity and light value) constantly and the real-time values will be shown on the LCD while both real-time and historical values will be shown on the web application. Secondly, when an RFID card is detected, it will populate the database with the UID and datetime value. And the green LED will be lit and a short buzz will be heard. If the RFID card is not detected properly, the red LED will be lit and a long buzz will be heard. Thirdly, the PiCamera will take an image of the entire greenhouse every 30 seconds and upload the image to AWS S3 bucket and populate database with device id, datetime value and the filename. The latest image belonging to greenhouse will be displayed on the greenhouse page of the web application. Image can be taken manually using a button on the web application. Lastly, the LEDs and buzzer can be controlled through the web application.

### Farm 1 RPi

Firstly, Farm 1 should populate the database with environment data (temperature, humidity and light value) constantly and the real-time values will be shown on the LCD while both real-time and historical values will be shown on the web application. Secondly, Farm 1 will constantly monitor the moisture level of the soil and pump water automatically when moisture level is considered dry. It also display messages on the LCD regarding the soil moisture. Thirdly, the PiCamera will take an image of the plant every hour and upload the image to AWS S3 bucket and populate database with device id, datetime value and the filename. The latest image belonging to farm 1 will be displayed on the farm 1 page of the web application. Image can be taken manually using a button on the web application. Lastly, the pump can be controlled through the web application.

### Farm 2 RPi

Firstly, Farm 2 should populate the database with environment data (temperature, humidity and light value) constantly and the real-time values will be shown on the LCD while both real-time and historical values will be shown on the web application. Secondly, Farm 2 will constantly monitor the moisture level of the soil and sends an email and SMS notification when moisture level is considered dry. It also display messages on the LCD regarding the soil moisture. Thirdly, the PiCamera will take an image of the plant every hour and upload the image to AWS S3 bucket and populate database with device id, datetime value and the filename. The latest image belonging to farm 2 will be displayed on the farm 2 page of the web application. Image can be taken manually using a button on the web application. Lastly, the buzzer can be controlled through the web application.

### Web Application

Firstly, the web application should be able to be accessed from any device and have a homepage with buttons to redirect users to different pages. Secondly, at the greenhouse page, it will display the real-time and historical values of temperature, humidity and light, the latest image of the greenhouse and the recent card access. It allows users to control the LEDs and buzzer of the greenhouse and take pictures manually. Thirdly, at the farm 1 page, it will display the real-time and historical values of temperature, humidity and light and the latest image of the plant. It allows users to control the pump and take pictures manually. Lastly, at the farm 2 page, it will display the real-time and historical values of temperature, humidity and light, the latest image of the plant. It allows users to control buzzer and take pictures manually. 

## Section 12 References

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
