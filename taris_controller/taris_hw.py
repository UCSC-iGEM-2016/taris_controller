from taris_reactor import Taris_Reactor as Reactor
import time
import sys
import os


def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def Setup_Bioreactor():
    cls()

    # Give time for sensors to power on

    x=1
    while x<5:
        if x==1:
            sys.stdout.write("Setting up sensors")
        else:
            sys.stdout.write(".")
        sys.stdout.flush() 
        time.sleep(1)
        x+=1
    print('\n')
    

    # Initial Parameters

    # I2C Addresses

    pH_sensor_address      = 0x63
    temp_sensor_address    = 0x66
    adc_address            = 0x48
    
    # Control parameters

    pwm_frequency = 75
    sample_frequency = 100 #Hz

    pH_def   = 5.0
    temp_def = 37.0 # Celsius

    # Default parameters for ADC settings

    i2c_bus  = 1
    adc_gain = 1

    inflow_ads_pin  = 0
    outflow_ads_pin = 1
    naoh_ads_pin    = 2
    filter_ads_pin  = 3
    
    
    newReactor = Reactor(adc_address,        \
                  i2c_bus,              \
                  pH_sensor_address,    \
                  temp_sensor_address,  \
                  pwm_frequency,        \
                  sample_frequency,     \
                  pH_def,               \
                  temp_def,             \
                  adc_gain,             \
                  inflow_ads_pin,       \
                  outflow_ads_pin,      \
                  naoh_ads_pin,         \
                  filter_ads_pin)
    
    return newReactor

def Print_Menu_Query():
    cls()
    print("Welcome to the UCSC iGEM 2016 Taris Bioreactor.")
    user_selection = str(raw_input('Please select from the options below:\n' +\
        '1.\tCalibrate Sensors\n' +\
        '2.\tSystem & Network Status\n' +\
        '3.\tStart Bioreactor\n' + '>>'))

    return user_selection

    
def Flowrate_to_PWM(input_rate):
    converted_value = 0.0431*input_rate - 0.5509
    return converted_value

def Form_Server_Path(server_ip, path):
    return server_ip + path    

def Network_Status():
    cls()
    print("TEST")
    raw_input("Press [ENTER] to return to main menu.")
    return False
def Run():
    user_input = Print_Menu_Query()
    
    # Calibrate Sensors
    if user_input == '1':
        Taris.Calibrate_Sensors()
        Run()

    # System & Network Status
    elif user_input == '2':
        Network_Status()
        print("BLEH")
        Run()

    # Start Bioreactor
    elif user_input == '3':
        Taris.Run_Bioreactor()
        Run()

# Begin setup

# Misc Variables

EXIT          = False

# Server settings

# server_ip     = Get_Server_IP()
server_ip       = 'localhost'
sensor_path     = '/sensorData' 
params_path     = '/paramsData'

send_path = Form_Server_Path(server_ip,sensor_path)
get_path  = Form_Server_Path(server_ip,params_path)

time.sleep(2)

Taris = Setup_Bioreactor()

Run()