from taris_adc import Taris_ADC as ADC
from taris_sensor import Taris_Sensor as Sensor
from pid_basic import PID
import requests
import os
import time
import sys
import json

def cls():
	os.system('cls' if os.name=='nt' else 'clear')

def Startup_Sequence_Wait():
	cls()

	x=1

	'''
	while x<5:
		if x==1:
			sys.stdout.write("Setting up sensors")
		else:
			sys.stdout.write(".")
		sys.stdout.flush() 
		time.sleep(1)
		x+=1
	print('\n')'''

def Print_Menu_Query():
	cls()
	print("Welcome to the UCSC iGEM 2016 Taris Bioreactor.")
	user_selection = str(input('Please select from the options below:\n' +\
		'1.\tCalibrate Sensors\n' +\
		'2.\tSystem & Network Status\n' +\
		'3.\tStart Bioreactor\n' + '>>'))

	return user_selection

def Calibrate_Sensors(pH_sensor, temp_sensor):
	cls()
	user_selection = str(input('Please select from the options below:\n' +\
		'1.\tCalibrate pH sensor\n' +\
		'2.\tCalibrate temp sensor\n' +\
		'3.\tCalibrate both temp and pH\n' + '>>'))
	if user_selection == '1':
		pH_sensor.pH_calibrateSensor()
	elif user_selection == '2':
		temp_sensor.temp_calibrateSensor()
	elif user_selection == '3':
		pH_sensor.pH_calibrateSensor()
		temp_sensor.temp_calibrateSensor()
		setup_temp = temp_sensor.getData()
		pH_compensateTemp(setup_temp)

def Status():
	cls()
	user_selection = input('\tThe temperature is:' + temp +\
	'\n\tThe pH is: \n')

def Run_Bioreactor(	sample_time,	\
					pH_end,			\
					pH_int_prev,	\
					pH_error_prev, 	\
				   	temp_end,		\
					temp_int_prev,	\
					temp_error_prev):

	cls()

# Get sensor values

	current_pH, current_temp = Check_Sensors(pH_sensor, temp_sensor)

# Run a PID on the temperature

	pid_basic(current_temp, temp_end, sample_time, temp_int_prev, temp_error_prev)

# Run a PID on the pH

	pid_basic(current_pH, pH_end, sample_time, pH_int_prev, pH_error_prev)

# Send server JSON data to update interface

	Send_JSON(server_ip, current_pH, current_temp, inflow, outflow, naoh, filt, heater)


# Get JSON data from server and update parameters


	
# Checks our beautiful sensors

def Check_Sensors(pH_sensor, temp_sensor):
	current_pH = pH_sensor.getData()
	current_temp = temp_sensor.getData()
	return current_pH, current_temp

# Check for new JSON and parse

def Get_JSON(server_ip):

	json_string = {'some': 'data'}
	r = requests.post(server_ip, data=json.dumps(json_string))

	# Parse JSON and write to parameters	
	json_parsed = json.loads(json_string)
	pH_end = json_parsed['pH']
	temp_end = json_parsed['temp']
	flowrate = json_parsed['flowrate']

	return  pH_end, temp_end, flowrate

# Send JSON to server

def Send_JSON(server_ip, current_pH, current_temp, inflow, outflow, naoh, filt, heater):

	json_string = {
    	'pH': current_pH,
    	'temp': current_temp,
    	'inflow': inflow,
		'inflow_pwm': inflow_pwm,
    	'outflow': outflow,
		'outflow_pwm': outflow_pwm,
    	'filter': filt,
		'filter_pwm': filt_pwm,
    	'naoh': naoh,
		'naoh_pwm': naoh_pwm,
    	'heater': heater,
		'heater_pwm': heater_pwm}

def Get_Server_IP():
	server_ip = str(raw_input("Enter server ip: "))
	return server_ip

# Misc Variables

EXIT = False
server_ip = Get_Server_IP()
pwm_frequency = 75
	
# Give sensors time to start

Startup_Sequence_Wait()

# I2C Addresses

pH_sensor_address	= 0x63
temp_sensor_address	= 0x66
adc_address			= 0x48

# Default parameters for ADC settings

i2c_bus  = 1
adc_gain = 1

# Set up ADC and initialize address

ads = ADC(adc_address, i2c_bus)
ads.setupADC()

# Set up Atlas Scientific sensors

temp_sensor = Sensor(temp_sensor_address,i2c_bus)
pH_sensor 	= Sensor(pH_sensor_address,i2c_bus)

print("Sensor setup complete.")

time.sleep(2)

START = False

# Check for initial user input

while not START:
	user_input = Print_Menu_Query()
	
	# Calibrate Sensors
	if user_input == '1':
		Calibrate_Sensors(pH_sensor,temp_sensor)

	# System & Network Status
	elif user_input == '2':
		Status()

	# Start Bioreactor
	elif user_input == '3':
		START = True


while START:
	Run_Bioreactor()
	Send_JSON()
	Get_JSON()



'''
	# Define JSON packet
	pi_json_string = {
    	'pH': taris.getPH(),
    	'temp': taris.getTemp(),
    	'inflow': taris.getInflow(),
    	'outflow': taris.getOutflow(),
    	'filter': taris.getFilter(),
    	'naoh': taris.getNaoh(),
    	'heater': taris.getHeater()
	}
'''
