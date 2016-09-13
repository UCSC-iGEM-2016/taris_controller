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
    
    def __init__(self, inPWM, outPWM, naohPWM, heaterPWM, Kp, Ki, Kd):
        self.inPWM       = inPWM
        self.outPWM      = outPWM
        self.naohPWM     = naohPWM
        self.heaterPWM   = heaterPWM
        
        self.inPIN       = 21        # Inflow motor default pin:    21
        self.outPIN      = 22        # Outflow motor default pin:   22
        self.naohPIN     = 23        # NaOH motor default pin:      23
        self.heaterPIN   = 17        # Heating element default pin: 17

        # PID Function Variables
        self.current_val      = 0.0
        self.end_val          = 0.0
        self.sample_time      = 0.0
        self.integral_prev    = 0.0
        self.error_prev       = 0.0
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

        # PI pH Variables
        self.desired_pH       = 7.0
        self.current_pH       = 0.0
        self.pH_Kp            = 0.0
        self.pH_Ki            = 0.0
        self.pH_error         = 0.0
        self.pH_sample_time   = 0.0
        self.pH_curr_time     = 0.0
        self.pH_prev_time     = 0.0
        self.pH_P             = 0.0
        self.pH_I             = 0.0
        self.pH_I_MAX         = 0.0
        self.pH_I_MIN         = 0.0

        # PI Temperature Variables
        self.desired_temp     = 24.0 # Celsius
        self.current_temp     = 0.0
        self.temp_Kp          = 0.0
        self.temp_Ki          = 0.0
        self.temp_error       = 0.0
        self.temp_sample_time = 0.0
        self.temp_curr_time   = 0.0
        self.temp_prev_time   = 0.0
        self.temp_P           = 0.0
        self.temp_I           = 0.0
        self.temp_I_MAX       = 0.0
        self.temp_I_MIN       = 0.0

        # initiate pi-blaster with only the four default pins above
        os.system("sudo pi-blaster --gpio 17,21,22,23")

    def set_PIN_at_PWM(self, PIN, PWM):
        PIN = str(PIN)
        PWM = str(PWM)
        print("Setting pin " + PIN + " to " + PWM + ".")
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

    def PI_Heater(self, input_temp):
        """
        """

        if input_temp > self.desired_temp:
            return 0
        
        self.current_temp = input_temp
        self.current_time = time.time()                           # Get current time
        if self.previous_time is 0:
            self.previous_time = self.current_time
        self.sample_time = self.current_time - self.previous_time # Get sample time
        self.previous_time = self.current_time

        self.temp_error = (self.current_temp - self.desired_temp)
        self.integral += (self.error * self.sample_time)
        self.temp_I = self.temp_Ki * self.integral
        self.temp_P = self.temp_Kp * self.error

        # Anti-windup solution
        if self.temp_I > self.temp_I_MAX:
            self.temp_I = self.temp_I_MAX
        elif self.temp_I < self.temp_I_MIN:
            self.temp_I = self.temp_I_MIN

	temp_PI = self.temp_P + self.temp_I
	return temp_PI

    def PID(self, current_val, end_val, sample_time, integral_prev, error_prev, sensor):
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

            # Define parameters for feedback mechanism
            error_curr = float(end_val) - float(current_val)
            integral = integral_prev + float(error_curr*sample_time) / self.Ki
            derivative = (error_curr - error_prev)/(sample_time * self.Kd)

            # Compute output from above parameters
            y = self.Kp * (error_curr + integral + derivative)

            error_prev = error_curr
            integral_prev = integral

            # pH settings
            if sensor == "pH":
                if error_curr <= 0:
                    y = 0

            # Temperature settings
            elif sensor == "temp":
                if error_curr < 0:
                    y = 0
                elif 10 < error_curr < 20:
                    y = 100 - 200/error_curr
                elif error_curr > 15:
                    y = 100
                    
            elif y < 0:
                y = 0
            
            scaling_factor = 10.0 # don't burn things down            
            y = y/scaling_factor
                
            print(sensor + " output: " + str(y) + ", " + str(integral) + " ," + str(error_curr))
            return (abs(y/100.0), error_prev, integral_prev)
        else:
            return 0

    def Bang_Bang(self, current_val, end_val, sample_time, integral_prev, error_prev, sensor):
        """
        """
        
