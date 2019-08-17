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

There are just 2 pins located on the LED:
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

#### Three LCD Screen
We will be using three 16x2 i2c LCD Screens for each Raspberry Pi. The LCD Screens will be used to dictate data readings on the physical screen:

-	Greenhouse – Temperature & Humidity
-	Farm 1 – Temperature & Humidity
-	Farm 2 – Temperature & Humidity

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
