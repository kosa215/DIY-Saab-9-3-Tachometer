# DIY Saab 9-3 Tachometer

## Motivation
A few months after buying my first manual transmission [vehicle](/images/saab_exterior.jpg) (a 2007 Saab 9-3 Aero), I was having a lot of fun with it but found myself with a problem I wanted to solve. In doing so I ended up learning a lot about CAN-networking, Raspberry Pi, and bluetooth communication.

## Big Idea
Occasionally while driving I would find myself wondering what gear I was in, especially if I hadn't recently changed gears. Yes, I could just remember. Yes, I could compare RPMs to vehicle speed in my head. Yes, I could look at the shifter and try to tell whether it was in 4th, or slightly to the right in 6th. But none of those solutions would let me tinker with my big boy toys.

So I set out to install a screen in my car that would show me what gear I am in. In each gear (1-6), when the gear is engaged there is a constant and unique ratio of engine RPM to vehicle speed (occasionally the ratio changes slightly due to a few factors but 99% of the time it will be consistent). By accessing the OBDII port, I can probably get instantaneous readings for the engine RPM and for the vehicle speed, so once I build everything I should be able to instantaneously estimate what gear I'm in. Since I need RPMs as part of the calculation for gear, I'll go ahead and throw in a digital tachometer to fill up the screen and make it look cooler.

## Materials Used
[Raspberry Pi 3](https://www.amazon.com/gp/product/B01MT4EA4D/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)  
[3.5 inch Touch Screen with Case](https://www.amazon.com/gp/product/B07N38B86S/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1)  
[Power Cable](https://www.amazon.com/gp/product/B01N336XEU/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)  
  
[Arduino Uno](https://www.amazon.com/Development-Microcontroller-ATmega328-ATMEGA16U2-Original/dp/B07R1H4BKK/ref=sr_1_6?keywords=arduino+uno&qid=1570579265&s=electronics&sr=1-6)  
[seeed CAN Shield](https://www.amazon.com/gp/product/B076DSQFXH/ref=ppx_yo_dt_b_asin_title_o04_s01?ie=UTF8&psc=1)  
[DB9-to-OBDII cable](https://www.amazon.com/gp/product/B01ETRINYO/ref=ppx_yo_dt_b_asin_title_o04_s01?ie=UTF8&psc=1)  

[Cheap bluetooth OBDII reader](https://www.amazon.com/gp/product/B01BY2CK32/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)

## Building the thing
I did a lot of things in order to get this thing done. I'll try to recount them chronologically.

### Step 1 - Design the tachometer and integrate it into Python.
Below is the what the information panel looks like on the car before modification. It's pretty basic - tachometer on the left, spedometer in the middle, some other gauges on the right, text display on the bottom, and some indicator lights throughout. 

![Sometimes shit happens.](/images/saab_dash.jpg)

The first thing I did was take a detailed picture of the tachometer, and trace it in Inkscape. Now I had a digital copy of the background of the gauge, as well as a digital copy of the needle. I applied a little styling, saved them both as separate files, then used the pygame module in python to draw them when I ran my Python script. I also wrote some code for rotating the needle based on an RPM value. The result is below.

![before and after.](/images/tach_compare.png)

### Step 2 - Get it onto the Raspberry Pi
This step was pretty simple. I was running Raspbian on the Pi, so all I had to do was clone my private git repository. After doing that I had the file on the Pi. Next I had to set up the Touch Screen and Case. After applying some elbow grease, I now had the Raspberry Pi inside the case, connected to the screen. I connected a wireless USB keyboard+mouse combo that I used for most of my in-vehicle development.

### Step 3 - Connect Arduino to Pi and OBDII 
Physically, the connection here goes:

OBDII port near brake pedal -> ODBII-to-DB9 cable -> CAN shield -> Arduino -> USB cable -> Raspberry Pi

The setup was kind of [messy](/videos/messy.gif) at this point, but I had what I needed to start messing around with the vehicle. I implemented a basic CAN reader [program](/code/CAN_reader/can_read.ino) using the MCP_CAN library. The program will monitor the OBDII port, and whenever it sees a CAN message, package it into a string and send that over a serial connection to the Raspberry Pi. I then wrote some [code](/code/CAN_reader/write_can_data_to_file.py) on the Raspberry Pi to watch for those packages and write them to a text file that I could review later.

### Step 4 - Reverse engineer CAN message locations
CAN messages are composed of a message identifier followed by some number of bytes of data (this is a simplification, but that's all you need to care about most of the time). So after running the setup from step 3 in-vehicle, I get a text file with a bunch of lines in it, and each line has a 3 digit number followed by some bytes in hex. The bytes contain information that the car's modules are passing to one another - a powertrain module might put a message on the bus that contains the coolant temperature in the first 4 bytes and engine RPM in the next 4 for example.
\
\
However, for some mostly good reasons, automotive OEMs don't tell the pulbic what each message means, how to decode it, units, or anything. So if you're DIYing it, you have to figure it out yourself unless someone else has already done so (shout out to [commaai/opendbc](https://github.com/commaai/opendbc), who have compiled a lot of that information for a variety of vehicles, but not for my Saab). 
\
\
The information I'm interested in for this project is engine RPM and vehicle speed, but while I had everything set up I figured I would map as much of the bus as I could in case I want something else in the future or if someone else does. I will say I found another bus I wrote out a test procedure and started taking data. Each of the maneuvers was attempting to isolate certain vehicle behaviors, and involved things like turning the steering wheel while at standstill, accelerating in a straight line, and pulling and releasing the park brake. Because I followed my procedure in order and on time, I was able to compare the CAN data with what I knew I was doing at a given time to learn more about what messages reacted to my behaviors.
\
\
To make comparison easier, I made a [GUI](/code/reverse_engineering.py) in python to help me rapidly review results. Basically the script would load a text file of CAN data, and then separate the messages so that those with the same message identifier were grouped together. It asks the user to select a message identifier, and a single byte or pair of bytes to review. It then plots the selected submessage data over time, at which point I reviewed each.
\

\
A lot of the reviewing was easy - many of the plots were meaningless noise, which would only make sense when viewed in a different way or combined with other bits. In others, I saw trends that resembled physical quantities - what looked like a speed profile, or a steering profile, or a brake pedal profile. I lucked out in that I was interpreting the bits in Big-Endian and got meaningful data. The messages could have been Little-Endian instead, in which case I would have had to interpret them the opposite direction, but they weren't, so I didn't. After some more experimentation, I arrived at my homegrown DIY 2007 Saab 9-3 CAN [map](/linktomap). I didn't completely finish that - there are some signals I couldn't decode or figure out what they were, but I got what I needed and more. Among other reasons, some submessages remain uncharted likely because they start or end in the middle of one of the bytes, or are composed of more than 2 bytes. 
\
\
What I found was that engine RPM seemed to match XXX , and vehicle speed seemed to match YYY. 


## Future tasks
-Hijack text-display on Saab panel to display the gear.
