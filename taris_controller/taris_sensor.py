import time
import io
import fcntl


class Taris_Sensor():
	
	def __init__(self, sensor_address, i2c_bus):

		self.i2c_bus = i2c_bus

		self.file_read = io.open("/dev/i2c-"+str(i2c_bus), "rb",buffering=0)
		self.file_write = io.open("/dev/i2c-"+str(i2c_bus),"wb",buffering=0)
	
	def sensorWrite(self, string):
		string += "\00"
		self.file_write.write(string)
		
		return True

	def sensorRead(self,num_bytes):
		sensor_data = str(self.file_read.read(num_bytes))
		
		if sensor_data.startswith("254"):
			sensor_data = str(self.file_read.read(num_bytes))
			response = filter(lambda x: x != '\x00', sensor_data)

        	if(ord(response[0]) == 1):
				char_list = map(lambda x: chr(ord(x) & ~0x80), list(response[1:]))
				return char_list
        	else:
				return False
		return False

	def pH_calibrateSensor(self):
		self.sensorWrite("Cal,clear")
		time.sleep(0.5)
		if self.sensorRead(2) != '1':
			print "Calibration failed!"
			return False

		input("Press Enter when pH 7 buffer is loaded")
		self.sensorWrite("Cal,mid")
		time.sleep(1.6)
		if self.sensorRead(2) != '1':
			print "Calibration failed!"
			return False

		input("Press Enter when pH 4 buffer is loaded")
		self.sensorWrite("Cal, low")
		time.sleep(1.6)
		if self.sensorRead(2) != '1':
			print "Calibration failed!"
			return False

		input("Press Enter when pH 10 buffer is loaded")
		self.sensorWrite("Cal, high")
		if self.sensorRead(2) != '1':
			print "Calibration failed!"
			return False

		time.sleep(0.5)
		if self.sensorRead(2) != "?CAL,3":
			print "Three point calibration incomplete!"
			cal_response = input("Press R to retry or Enter to exit.")
			if cal_response == "R":
				self.pH_calibrateSensor()
			
			else:
				return False
		return True

	def temp_calibrateSensor(self,temp):
		self.sensorWrite("Cal,clear")
		time.sleep(0.5)

		input("Enter temperature of calibration solution: ")
		self.sensorWrite("Cal," + str(temp))
		time.sleep(0.5)
		if self.sensorRead(2) != '1':
			print "Calibration failed!"
			return False

		time.sleep(0.5)
		if self.sensorRead(2) != "?CAL,1":
			print "One point temperature calibration incomplete!"
			cal_response = input("Press R to retry or Enter to exit.")
			if cal_response == "R":
				temp_calibrateSensor()
			
			else:
				return False
		return True

	def getData(self):

		read_bytes = 7

		self.sensorWrite("R")
		time.sleep(1.5)

		sensor_data = self.sensorRead(read_bytes)

		if sensor_data.startswith("254"):
			while not sensor_data.startswith('1'):
				if sensor_data.startswith('2'):
					return False
				sensor_data = self.sensorRead(read_bytes)

		return sensor_data[1:]

	def pH_compensateTemp(self,temp):
		self.sensorWrite("T," + str(temp))
		time.sleep(0.3)

		comp_status = self.sensorRead(2)
		
		if comp_status != '1':
			print "Temperature compensation failed!"
			return False

		else:
			print "Temperature compensation set for: " + str(temp) + "C"

		return False

	
	def lockProtocol(self,command):

		print "1.\tDisconnect power to device and any signal wires.\n2.\tShort PRB to TX.\n3.\tTurn device on and wait for LED to change to blue.\n4.\tRemove short from PRB to TX, then restart device.\n5.\tConnect data lines to Raspberry Pi I2C pins."

		input("Press Enter when this is complete.")

		input("Press Enter to prevent further changes to device configuration.")
		command_message = "PLOCK," + str(command)

		self.sensorWrite(command_message)
		time.sleep(0.3)
		lock_status = self.sensorRead(read_bytes)
		if lock_status == "?PLOCK,1":
			print "Sensor settings locked."
			return_code = 1
		elif lock_status == "?PLOCK,0":
			print "Sensor settings unlocked."
			return_code = 0
		else:
			print "False locking sensor settings."
			return False

		return return_code

	


	
	
		

		


		
