#!/usr/bin/env python

import os

# Uses pi-blaster to run a PWM from the raspberry pi pins.
# Once pi-blaster is installed on the pi, bash commands 
# can control the PWM output of individual pins.
# 
# Bash examples (taken from https://github.com/sarfata/pi-blaster): 
#
# This command sets pin 17 to 100%:
#### > echo "17=1" > /dev/pi-blaster 
#
# This command sets pin 17 to 20%:
#### > echo "17=0.2" > /dev/pi-blaster 
#
# This command sets pin 17 to 0%:
#### > echo "17=0" > /dev/pi-blaster
#
# This command releases a pin for use as a GPIO or an input again:
#### > echo "release 17" > /dev/pi-blaster
# 
# To override the default list of supported GPIO pins and specify 
# fewer (or more) you can specify a comma separated list of GPIO 
# numbers. This is also the default list:
#### > ./pi-blaster --gpio 4,17,18,27,21,22,23,24,25
#
# To use the BCM2835's PCM peripheral instead of its PWM peripheral
# to time the DMA transfers, pass the option:
#### > ./pi-blaster --pcm
# 
# To invert the pulse (off = pin HIGH, pulse = pin LOW), use:
#### > ./pi-blaster --invert
# 
# To keep pi-blaster running in the foreground without running 
# as a daemon use:
#### > ./pi-blaster -D
# 
# To view help or version information, use:
#### > ./pi-blaster --help
#### > ./pi-blaster --version

class Taris_PWM():
    
    def __init__(self, inPWM, inPIN, outPWM, outPIN, naohPWM, naohPIN, heaterPWM, heaterPIN):
        self.inPWM       = inPWM
        self.inPIN       = inPIN        # inflow motor default pin:    21
        self.outPWM      = outPWM
        self.outPIN      = outPIN       # outflow motor default pin:   22
        self.naohPWM     = naohPWN
        self.naohPIN     = naohPIN      # NaOH motor default pin:      23
        self.heaterPWM   = heaterPWM
        self.heaterPIN   = heaterPIN    # heating element default pin: 24

        # initiate pi-blaster with only the four default pins above
        os.system("./pi-blaster --gpio 21,22,23,24")

    def set_PIN_at_PWM(self, PIN, PWM):
        os.system("echo '" + PIN + "=" + PWM + "' > /dev/pi-blaster")

    def TEST_set_PIN_at_PWM(self, PIN, PWM):
        # writes pi-blaster commands to the FIFO file that assign a given PWM to a given pin.
        # this is the default method of communication for pi-blaster
        file_path = path.relpath("/dev/pi-blaster")
        f = open(file_path,"w")
        f.write(PIN + "=" + PWM)
        f.close()
























