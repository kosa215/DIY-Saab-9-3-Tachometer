# DIY Saab 9-3 Tachometer

## Motivation
A few months after buying my first manual transmission [vehicle](/images/saab_exterior.jpg), I was having a lot of fun with it but found myself with a problem I wanted to solve. At the same time, I knew the project would involve learning more about CAN-networking, Raspberry Pi, and bluetooth communication.

Below is the what the information panel looks like on the car before modification. It's pretty basic - tachometer on the left, spedometer in the middle, some other gauges on the right, text display on the bottom, and some lights throughout. 

![Sometimes shit happens.](/images/saab_dash.jpg)

Occasionally while driving I would find myself wondering what gear I was in, especially if I hadn't recently changed gears. Yes, I could just remember. Yes, I could compare RPMs to vehicle speed in my head. Yes, I could look at the shifter and try to tell whether it was in 4th, or slightly to the right in 6th. But none of those solutions would let me tinker with my big boy toys. So I decided I would make my own digital tachometer, that also displays what gear you are in. 

# Materials Used
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
The first thing I did was take a detailed picture of my car's tachometer, and trace it in Inkscape. Now I had a digital copy of the background of the gauge, as well as a digital copy of the needle. I applied a little styling, saved them both as separate files, then used the pygame module in python to draw them when I ran my Python script. The result is below.

![before and after.](/images/tach_compare.png)

### Step 2 - Get it onto the Raspberry Pi
This step was pretty simple. I was running Raspbian on the Pi, so all I had to do was clone my private git repository. After doing that I had the file on the Pi. Next I had to set up the Touch Screen and Case. After applying some elbow grease, I now had the Raspberry Pi inside the case, connected to the screen. I connected a USB

## Future tasks
-Hijack text-display on Saab panel to display the gear.
