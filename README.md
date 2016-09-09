UCSC's Taris Bioreactor Controller Software
===========================================

This project allows for the control of UCSC's Taris bioreactor (an autonomous fermentor designed for growing bacteria/yeast).

This reactor controls temperature and pH and operates in a continuous batch mode as a chemostat.  More details of the project can be found here: LINK.

This software is entirely written in python 2.7 and designed to be run on a Raspberry Pi 3.  In addition, this software can optionally be used with UCSC's taris server software to stream live data to a website or give the user remote control from a smartphone.

## Default Pin Connections and Links to Required Hardware

All circuit designs and hardware schematics are available for free and open-source use to anyone with the desire to construct a bioreactor themselves (see below).

* The bioreactor parts list can be found here: LINK.
* The raw diptrace file (the electrical circuit's schematic) can be found here: LINK.
* The assembly manual can be found here: LINK.
* The user manual can be found here: LINK.

The default GPIO numbers are given in the diagram below: IMAGE.

## Running the Software

Doing such and such should install the following dependencies:

* Adafruit Thing
* I2C Thing

To run the program:

    sudo python /path/to/software/taris_hw.py

After some initialization text, the output should look like:

    "Welcome to the UCSC iGEM 2016 Taris Bioreactor.
    
    Please select from the options below:
    1. Calibrate Sensors
    2. System & Network Status
    3. Motor Control and Tests
    4. Start the Bioreactor"

## Comments and Caveats:
* Before running the software, one can check i2c connections with the command:
    i2cdetect -y 1
* If run on a raspberry pi 2, the I2C bus is 0 instead of 1 (above), so this must be changed in the "taris_hw.py" code, and additionally the above command becomes:
    i2cdetect -y 0
* It is necessary to calibrate PID feedback by following this manual: LINK.
* It is also necessary to calibrate the sensors by following this manual: LINK.

## Want to support this project?

Potentially in the future we may offer project kits to assemble our bioreactor, but as of now there is no one available to do so.  If you do happen to construct our bioreactor, please send us photos!  Pull requests and writing code for the features you would like to see are also very nice and appreciated.

## Acknowledgements

This work made possible with thanks to the following UCSC iGEM software/bioreactor contributors:

* Henry Hinton (https://github.com/hhinton)
* Austin York (https://github.com/akyork)
* Colin Hortman (https://github.com/colinhortman)
* Andrew Blair (https://github.com/apblair)
* Lon Blauvelt (https://github.com/DailyDreaming)

We would also like to thank:

* [Lady Ada (Limor Fried)](http://www.ladyada.net/) of [Adafruit](https://www.adafruit.com/).
* [Sarfata (Thomas Sarlandie)](http://www.sarfata.org/about.html) the author of [pi-blaster](https://github.com/sarfata/pi-blaster).

## License

This software is published under a GNU GENERAL PUBLIC LICENSE.
