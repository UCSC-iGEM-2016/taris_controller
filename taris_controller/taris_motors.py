#!/usr/bin/env python

from __future__ import print_function    # reconciles printing between python2 and python3
import os
import io

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

#PINd = 22
#PWMd = 0
#PINd = str(PINd)
#PWMd = str(PWMd)
#os.system("echo '" + PINd + "=" + PWMd + "' > /dev/pi-blaster")

class Taris_Motors():
    
    def __init__(self, inPWM, outPWM, naohPWM, heaterPWM):
        self.inPWM       = inPWM
        self.outPWM      = outPWM
        self.naohPWM     = naohPWM
        self.heaterPWM   = heaterPWM
        
        self.inPIN       = 21        # inflow motor default pin:    21
        self.outPIN      = 22        # outflow motor default pin:   22
        self.naohPIN     = 23        # NaOH motor default pin:      23
        self.heaterPIN   = 24        # heating element default pin: 24

        self.current_val      = 0.0
        self.end_val          = 0.0
        self.sample_time      = 0.0
        self.integral_prev    = 0.0
        self.error_prev       = 0.0

        # initiate pi-blaster with only the four default pins above
        os.system("sudo ./pi-blaster/pi-blaster --gpio 21,22,23,24")

    def set_PIN_at_PWM(self, PIN, PWM):
        PIN = str(PIN)
        PWM = str(PWM)
        os.system("echo '" + PIN + "=" + PWM + "' > /dev/pi-blaster")

    def TEST_set_PIN_at_PWM(self, PIN, PWM):
        # attempts to write pi-blaster commands to the FIFO file
        # this is the default method of communication for pi-blaster
        # not currently used
        PIN = str(PIN)
        PWM = str(PWM)
        file_path = os.path.relpath("/dev/pi-blaster")
        f = open(file_path,"w")
        f.write(PIN + "=" + PWM)
        f.close()

    def PID(self, current_val, end_val, sample_time, integral_prev, error_prev):
        """
        PID is a feedback control algorithm that determines the output of a system
        input x(t) to stabilize future outputs x(t+n). This allows for regulated
        pulse width modulation (PWM) for "locking" a system to a desired value.

        :param current_val: current input value
        :param end_val: desired system value
        :param sample_time: sampling rate (run PID every x seconds)
        :param integral_prev: previous integral value
        :param error_prev: previous error value
        :return: system value, previous error, integral error
        """
        if current_val != None:
            if integral_prev == None:
                integral_prev = 0.0
                error_prev = 0.0
                current_val = 0.0

            # Gain constants
            kp = 1
            ki = 1
            kd = 1

            # Define parameters for feedback mechanism
            error_curr = int(end_val) - int(current_val)
            integral = integral_prev + float(error_curr*sample_time) / ki
            derivative = (error_curr - error_prev)/(sample_time * kd)

            # Compute output from above parameters
            y = kp * (error_curr + integral + derivative)

            error_prev = error_curr
            integral_prev = integral

            return (y, error_prev, integral_prev)
        else:
            return 0
