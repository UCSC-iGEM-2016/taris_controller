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
        time.sleep(0.5)
        x+=1
    print('\n')
    

    # Initial Parameters for setting up the bioreactor

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
    naoh_ads_pin    = 3
    filter_ads_pin  = 2
    
    # Server settings
    server_address = "http://128.114.62.72:5000" # austin
    #server_address = "http://169.233.176.10:5000" # colin
    server_post_path = "/currentRecieve"
    server_pull_path = "/currentPost"
    
    print("Setting server post path to: " + server_address + server_post_path)    
    
    newReactor = Reactor(adc_address,   \
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
                  filter_ads_pin,       \
                  server_address,       \
                  server_post_path,     \
                  server_pull_path)
    
    time.sleep(1)
    
    print("\nSetting up reactor on I2C bus %d...\n\
    ADS1115 (%x):\n\tGain: %d\n\t[IN|OUT|NAOH|FILTER]=[%d|%d|%d|%d]\n\
    EZO pH  (%x): Calibration required.\n\
    EZO RTD (%x): Sampling at 1Hz.\n\
    PWM frequency set to %dHz." %\
        (i2c_bus,\
        adc_address,adc_gain,inflow_ads_pin,outflow_ads_pin,naoh_ads_pin,filter_ads_pin,\
        pH_sensor_address,temp_sensor_address,pwm_frequency))
        
    
    time.sleep(3)    
    
    return newReactor

def Print_Menu_Query():
    '''Main bioreactor UI menu.'''    
    
    cls()
    print("Welcome to the UCSC iGEM 2016 Taris Bioreactor.")
    
    user_selection = str(raw_input('Please select from the options below:\n\
    1.\tCalibrate Sensors\n\
    2.\tSystem & Network Status\n\
    3.\tStart Bioreactor\n>>'))

    return user_selection
    
def Run():
    '''Checks main menu and resulting user input.'''
    
    user_input = Print_Menu_Query()
    
    # Calibrate Sensors
    if user_input == '1':
        Taris.Calibrate_Sensors()
        Run()

    # System & Network Status
    elif user_input == '2':
        print("BLEH")
        Run()

    # Start Bioreactor
    elif user_input == '3':
        Taris.Run_Bioreactor()
        Run()

time.sleep(2)

Taris = Setup_Bioreactor()

Run()
