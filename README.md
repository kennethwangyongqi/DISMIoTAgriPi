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
![Alt text](https://github.com/kennethwangyongqi/DISMIoTAgriPi/blob/master/README%20images/dht11sensor.jpg)

The DHT11 is a low cost digital temperature & humidity sensor that is capable of sensing the surrounding atmosphere using a capacitive humidity sensor and a thermistor. The reading will be signaled out onto the data pin and is fairly simple to use. We will be using one DHT11 sensor on each of the Raspberry Pi as each of the breadboard will be located on a different location. The DHT11 has be added with a 10k ohms resistor to supress the power, or else it will spoil the sensor.

There are 4 pins located on the DHT11:
•	VCC – connect it to 3v3 power
•	DATA – connect it to the GPIO value
•	NC – Stands for No Connection
•	GND – connect it to the ground

The fritzing diagram for setup will be the same for the other DHT11 and should look like this:


### Two LED 5mm Lights

There will be two different LED lights used to indicate for the RFID sensor entry. Green is for access granted and red is for access denied. 

There are just 2 pins located on the LED:
•	Connect the longer leg pin with blue jumper wire to the GPIO value
•	Connect the shorter leg pin to a 330 ohms resistor and to GND port with black jumper wire

The fritzing diagram setup should look like this for the greenhouse Raspberry Pi:

### One RFID/ NFC MFRC522 Card Reader Module

We will be using RFID card/tags with a RFID/NFC MFRC522 card reader module that is attached to the greenhouse Raspberry Pi to track, identify and manage access control.

There are 9 pins located on the MFRC522 card reader module and we will only be using 7 of them:

| MFRCF522 pin |	Connect |	RPi pin |	Jumper color |
| ------------ | -------- | ------- | ------------ |
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

