#!/usr/bin/python

from __future__ import print_function
import io         # used to create file streams
import fcntl      # used to access I2C parameters like addresses

import time       # used for sleep delay and timestamps


class Taris_Sensor():

    def __init__(self, address, bus):
        # open two file streams, one for reading and one for writing
        # the specific I2C channel is selected with bus
        # it is usually 1, except for older revisions where its 0
        # wb and rb indicate binary read and write
        self.file_read = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
        self.file_write = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)

        # initializes I2C to either a user specified or default address
        self.set_i2c_address(address)
        
        self.long_timeout = 1.5         	# the timeout needed to query readings and calibrations
        self.short_timeout = .5         	# timeout for regular commands
        
    def set_i2c_address(self, addr):
        # set the I2C communications to the slave specified by the address
        # The commands for I2C dev using the ioctl functions are specified in
        # the i2c-dev.h file from i2c-tools
        I2C_SLAVE = 0x703
        fcntl.ioctl(self.file_read, I2C_SLAVE, addr)
        fcntl.ioctl(self.file_write, I2C_SLAVE, addr)

    def write(self, cmd):
        # appends the null character and sends the string over I2C
        cmd += "\00"
        self.file_write.write(cmd)

    def read(self, num_of_bytes=31):
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
        self.sensorWrite("I")
        time.sleep(0.3)
        device_ID = self.sensorRead(22)
    
        if device_ID.startswith("?I"):
            print("Connected sensor: " + str(device_ID)[5:])
        else:
            raw_input("EZO not connected: " + device_ID)
            

    def close(self):
        self.file_read.close()
        self.file_write.close()

    def getData(self):
        data = self.query("R")
        return float(data)
        
    def pH_calibrateSensor(self):
        self.query("Cal,clear")
        if self.sensorRead(2) != '1':
            print("Calibration failed!")
            return False

        input("Press Enter when pH 7 buffer is loaded")
        q = self.query("Cal,mid")
        if q != '1':
            print("Calibration failed!")
            return False

        input("Press Enter when pH 4 buffer is loaded")
        q = self.query("Cal, low")
        if q != '1':
            print("Calibration failed!")
            return False

        input("Press Enter when pH 10 buffer is loaded")
        q = self.query("Cal, high")
        if q != '1':
            print("Calibration failed!")
            return False

        q = self.query("Cal,?")

        if q != "?CAL,3":
            print("Three point calibration incomplete!")
            cal_response = input("Press R to retry or Enter to exit.")
            if cal_response == "R":
                self.pH_calibrateSensor()
            else:
                return False
                
        return True

    def temp_calibrateSensor(self):
        q = self.query("Cal,clear")
        
        if q != "?CAL,1":
            print("One point temperature calibration incomplete!")
            cal_response = input("Press R to retry or Enter to exit.")
            if cal_response == "R":
                self.temp_calibrateSensor()
            else:
                return False
        return True

    def pH_compensateTemp(self,temp):
        comp_status = self.query("T," + str(temp))
        
        if comp_status != '1':
            print("Temperature compensation failed!")
            return False

        else:
            print("Temperature compensation set for: " + str(temp) + "C")

        return False

    
    
    def lockProtocol(self,command):
        '''Not currently working'''
        
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

    


    
    
        

        


        
