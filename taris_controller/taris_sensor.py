#!/usr/bin/python

from __future__ import print_function
import io         # used to create file streams
import fcntl      # used to access I2C parameters like addresses

import time       # used for sleep delay and timestamps


class Taris_Sensor():
    ''' This object holds all required interface data for the Atlas Scientific \
    EZO pH and RTD sensors. Built off of the base library, with new functions \
    added for calibration and additional testing. '''
    def __init__(self, address, bus):
        # open two file streams, one for reading and one for writing
        # the specific I2C channel is selected with bus
        # it is usually 1, except for older revisions where it's 0
        # wb and rb indicate binary read and write
        self.file_read = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
        self.file_write = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)

        # initializes I2C to either a user specified or default address
        self.set_i2c_address(address)
        
        self.long_timeout = 1.5         	# the timeout needed to query readings and calibrations
        self.short_timeout = .5         	# timeout for regular commands
        
    def set_i2c_address(self, addr):
        '''Set the I2C communications to the slave specified by the address. \
        The commands for I2C dev using the ioctl functions are specified in \
        the i2c-dev.h file from i2c-tools'''
        I2C_SLAVE = 0x703
        fcntl.ioctl(self.file_read, I2C_SLAVE, addr)
        fcntl.ioctl(self.file_write, I2C_SLAVE, addr)

    def write(self, cmd):
        '''Writes a command to the sensor.'''
        # appends the null character and sends the string over I2C
        cmd += "\00"
        self.file_write.write(cmd)

    def read(self, num_of_bytes=31):
        '''Reads data from the sensor and parses the incoming response.'''
        # reads a specified number of bytes from I2C, then parses and displays the result
        res = self.file_read.read(num_of_bytes)         # read from the board
        response = filter(lambda x: x != '\x00', res)     # remove the null characters to get the response
        if ord(response[0]) == 1:             # if the response isn't an error
            # change MSB to 0 for all received characters except the first and get a list of characters
            char_list = map(lambda x: chr(ord(x) & ~0x80), list(response[1:]))
            # NOTE: having to change the MSB to 0 is a glitch in the raspberry pi, and you shouldn't have to do this!
            return ''.join(char_list)     # convert the char list to a string and returns it
        else:
            return "Error " + str(ord(response[0]))

    def query(self, string):
        '''For commands that require a write, a wait, and a response. For instance, \
        calibration requires writing an initial CAL command, waiting 300ms, \
        then checking for a pass/fail indicator message.'''
        # write a command to the board, wait the correct timeout, and read the response
        self.write(string)

        # the read and calibration commands require a longer timeout
        if((string.upper().startswith("R")) or
           (string.upper().startswith("CAL"))):
            time.sleep(self.long_timeout)
        else:
            time.sleep(self.short_timeout)

        return self.read()


    def verify(self):
        '''Verifies that the sensor is connected, also returns firmware version.'''
        device_ID = self.query("I")
    
        if device_ID.startswith("?I"):
            print("Connected sensor: " + str(device_ID)[3:])
        else:
            raw_input("EZO not connected: " + device_ID)
            
    def close(self):
        '''Closes the sensor's filestream, not usually required.'''
        self.file_read.close()
        self.file_write.close()

    def getData(self):
        '''Gets data from sensor reading as a float.'''
        data = self.query("R")
        return float(data)
        
    def pH_calibrateSensor(self):
        '''Performs pH sensor calibration using included buffers.'''
        
        
        # Clear previous calibration data
        print("Starting pH sensor calibration...")
        q = self.query("Cal,clear")
        if q != '1':
            print("Calibration failed with response " + q)
            time.sleep(2)
            return False

        # Midpoint calibration. This will also reset previous data.
        input("Press Enter when pH 7 buffer is loaded")
        q = self.query("CAL,MID")
        if q != '1':
            print("Calibration failed with response " + q)
            time.sleep(2)
            return False

        # Lowpoint calibration
        input("Press Enter when pH 4 buffer is loaded")
        q = self.query("CAL,LOW")
        if q != '1':
            print("Calibration failed with response " + q)
            time.sleep(2)
            return False

        # Highpoint calibration
        input("Press Enter when pH 10 buffer is loaded")
        q = self.query("CAL,HIGH")
        if q != '1':
            print("Calibration failed with response " + q)
            time.sleep(2)
            return False

        q = self.query("Cal,?")

        # Check that 3-point calibration is complete, otherwise return ERROR
        if q != "?CAL,3":
            print("Three point calibration incomplete!")
            cal_response = raw_input("Enter 'R' to retry or Enter to exit.")
            if cal_response == "R" or cal_response == "r":
                self.pH_calibrateSensor()
            else:
                return False
                
        return True

    def temp_calibrateSensor(self):
        '''Calibrates the temperature sensor. Requires an external thermometer.'''
        
        print("Clearing previous calibration.")
        q = self.query("Cal,clear\0x0d")
        
        if q == "1":
            cal_temp = raw_input("Enter room temperature.")
            q = self.query("Cal,"+str(cal_temp))
            
            if q == "1":
                
                q = self.query("Cal,?")
                if q == "?CAL,1":
                    print("One point temperature calibration complete!")
                    return True
                
                elif q == "?CAL,0":
                    print("One point temperature calibration incomplete!")
                    cal_response = raw_input("Enter R to retry or Enter to exit.")
                    if cal_response == "R" or cal_response == "r":
                        self.temp_calibrateSensor()
                    else:
                        return False
                else:
                    return False
            else:
                print("Could not set new calibration temperature.")
                time.sleep(1)
                return False
        else:
            print("Could not clear RTD sensor.")
            time.sleep(1)
            return False
            
            
        return False

    def pH_compensateTemp(self,temp):
        '''Compensates the pH sensor for temperature, is used in conjunction with \
        a reading from the RTD sensor.'''
        comp_status = self.query("T," + str(temp))
        
        if comp_status != '1':
            print("Temperature compensation failed!")
            return False

        else:
            print("Temperature compensation set for: " + str(temp) + "C")

        return False

    
    
    def lockProtocol(self,command):
        '''Not currently working. Normally used for locking some of the \
        internal parameters (e.g. baud rate for UART mode).'''
        
        read_bytes = 9

        print("1.\tDisconnect power to device and any signal wires.\n\
        2.\tShort PRB to TX.\n\
        3.\tTurn device on and wait for LED to change to blue.\n\
        4.\tRemove short from PRB to TX, then restart device.\n\
        5.\tConnect data lines to Raspberry Pi I2C pins.")

        input("Press Enter when this is complete.")

        input("Press Enter to prevent further changes to device configuration.")
        command_message = "PLOCK," + str(command)

        self.sensorQ(command_message)
        time.sleep(0.3)
        
        lock_status = self.sensorRead(read_bytes)
        if lock_status == "?PLOCK,1":
            print("Sensor settings locked.")
            return_code = 1
        elif lock_status == "?PLOCK,0":
            print("Sensor settings unlocked.")
            return_code = 0
        else:
            print("False locking sensor settings.")
            return False

        return return_code

    


    
    
        

        


        
