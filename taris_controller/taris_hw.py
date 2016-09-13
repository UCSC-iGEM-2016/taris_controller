################################################################
##............................................................##
##............................................................##
##.ZZZZZ.....ZZZZZ....ZZZZZZZZZZ...ZZZZZZZZZZ.....ZZZZZZZZZ+..##
##.ZZZZZ.....ZZZZZ..:ZZZZZZZZZZ...ZZZZZZZZZZ:...$ZZZZZZZZZZ...##
##.ZZZZZ.....ZZZZZ.=ZZZZZ=....Z..ZZZZZ.........ZZZZZZ.....Z...##
##.ZZZZZ.....ZZZZZ.ZZZZZ.........ZZZZZ:........ZZZZZ..........##
##.ZZZZZ.....ZZZZZ~ZZZZ,..........ZZZZZZZZ....:ZZZZ...........##
##.ZZZZZ.....ZZZZZ?ZZZZ............ZZZZZZZZZ~.?ZZZZ...........##
##.ZZZZZ.....ZZZZZ.ZZZZZ...............ZZZZZZ..ZZZZ:..........##
##.,ZZZZZ....ZZZZZ.ZZZZZ.................ZZZZ$.ZZZZZ..........##
##..ZZZZZZZZZZZZZZ..ZZZZZZZZZZZ$.ZZZZZZZZZZZZ...ZZZZZZZZZZZ,..##
##...ZZZZZZZZZZZZZ...ZZZZZZZZZZZ.ZZZZZZZZZZZZ....ZZZZZZZZZZZ..##
##......~ZZZ$=..........ZZZZZZ+....ZZZZZZZ..........ZZZZZZ+...##
##............................................................##
##                                                            ##
##                        .MM..                               ##
##                 .       .+..                               ##
##                 . .      ZI..                              ##
##                 M,N.... ..M+=..                            ##
##                 ..=?$......NO8.                            ##
##                     :MZI=..,.M+8..    .                    ##
##                    ....MM7M?+I?++DMMMM.                    ##
##                  .   . M++++ZNM+++++8..                    ##
##                  ..IMMM88MM++++++++++M.                    ##
##               .7MD88MMMMMMM+++++++++++$...                 ##
##              . .MMMMMMMMMMM+++++++++++I...                 ##
##                 .Z7++++++=++I++++++++++M,.                 ##
##                 .M+++++++++$++++++++++++M.                 ##
##                .N+++++++++M++++++++++++?7$                 ##
##               .+++++++++$MDZ+++++++++++D+M                 ##
##              ..M++++++$O+++?+++++++++++7D+MZ.              ##
##              ..INI+Z8IMMMDMMM$+++++++++++O+MI              ##
##                 ...:... ... ..M?++++++++++++M~ .           ##
##                                ~M++++++++++++M:. ..        ##
##                               ..M++++++++++++MM            ##
##                 . . .            :+++++++++++++?M..        ##
##               M.... $           . ?++++++++++++++M.        ##
##           ..   DMO.D.  ..      .  $+++++++++++++++M..      ##
##             ONMMN:O  .           ,+++++++++++++++++Z~.     ##
##           .,MM.MMMMM  Z....=~Z.$.Z++++++++++++++++++7:.    ##
##           :MMMMMMMOZM.  .:MMNNDM+++++++8+++++++++++++$..   ##
##           .MMMMMMMM,OM  DIMNOM8N8Z+++++$++++++++++++++N?.  ##
##             :MN MMMM$?N.DM=NI.8ZNMI+$D7=+++++++++++++++I~  ##
##               M?Z7NMMOM ,7O..D++++++++++++++++++++++++++M. ##
##            .  ?MMMM:MMMM .. 7+OMMMIO8?$DMMN$++++++++++++?+ ##
##              ..MMMMMMMMM+.  DMMMM7ZZ8+?++++++++++++++++++M.##
##        .......D7III$$DMMMM8MMMMMMMMMM++++++++++++++++++++M~##
##        ..~N+++++++++++++++7NMMMMMD$I+++++++++++++++++++++NI##
##     ....$++++++++++++++++++++++I77+++++++++++++++++++++++N7##
##       .$+++++++++++++++++++++++++++++++++++++++++++++++++M,##
##  ....=8+++++++++++++++++++++++++++++++++++++++++++++I++++M ##
##  .. ?+?7++++++++++++++++++++++++++++++++++++++++++++M+++M. ##
##  ..M+++M7++++++++++++++++++++++++++++++++++++++++++++++IM  ##
##  ..M++++NM?+++++++++++++++++++++++++++++++++++++++M+++OM.  ##
##  ..MM++++++MMO+++$MMMMMO8M$I8Z8MO++++++++++=++++7++++M. .  ##
##  ..M+NI++++++8M?IIIIII7III7I7I7MM=ODO++++++++M$M+++NM...   ##
##....Z++++$7+++++M8IIIIIIIIIIIIIIIIII$M++8+++7MN+++MM..      ##
##..~+MM++++8N?++++8M8DO$IIIIIIIIIIIIIIIIIOM++++++ZOM..       ##
##MMMMZ??IZMO++M7++++M. .........,+IMD$7I7OODMMIIN+Z$++MMMZ   ##
##  .........:M++++++M.  ............. ........ ........  .   ##
##            ...MM?+M                                        ##
##           .....NN7                                         ##
##                                                            ##
################################################################

from __future__ import print_function    # Reconciles printing between python2 and python3
from taris_reactor import Taris_Reactor as Reactor
import time
import sys
import os


def cls():
    # Blanks the terminal screen when used
    os.system('cls' if os.name=='nt' else 'clear')

def Setup_Bioreactor():
    cls()

    x=1
    while x<5:
        if x==1:
            sys.stdout.write("Setting up the sensors")
        else:
            sys.stdout.write(".")
        sys.stdout.flush() 
        time.sleep(0.5)
        x+=1
    print('\n')
    
    # Initial parameters for setting up the bioreactor

    # I2C addresses
    pH_sensor_address      = 0x63
    temp_sensor_address    = 0x66
    adc_address            = 0x48
    
    # Control parameters
    pwm_frequency          = 75   # Hz
    sample_frequency       = 100  # Hz
    pH_def                 = 7.0
    temp_def               = 75.0 # Fahrenheit

    # Default ADC settings
    i2c_bus                = 1    # 0 on older pi's
    adc_gain               = 1

    inflow_ads_pin         = 0
    outflow_ads_pin        = 1
    naoh_ads_pin           = 3
    filter_ads_pin         = 2
    
    # Server settings
    server_address = "http://128.114.62.72" # The UCSC SOE server
    server_post_path = "/currentRecieve"
    server_pull_path = "/currentPost"
    
    print("Setting server POST path to: " + server_address + server_post_path)
    print("Setting server GET path to: " + server_address + server_pull_path)
    
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
    ADS1115 (%x):\n\t\
    Gain: %d\n\t\
    [IN|OUT|NAOH|FILTER]=[%d|%d|%d|%d]\n\
    EZO pH Sensor  (%x): Calibration required.\n\
    EZO Temperature Sensor (%x): Sampling at 1Hz.\n\
    PWM frequency set to %dHz." %\
        (i2c_bus,\
        adc_address,\
        adc_gain,\
        inflow_ads_pin,\
        outflow_ads_pin,\
        naoh_ads_pin,\
        filter_ads_pin,\
        pH_sensor_address,\
        temp_sensor_address,\
        pwm_frequency))
            
    time.sleep(3)    
    
    return newReactor

def Print_Menu_Query():
    '''Main bioreactor UI menu.'''
    
    cls()
    print("Welcome to the UCSC iGEM 2016 Taris Bioreactor.\n")
    
    user_selection = str(raw_input('Please select from the options below:\n\
    1.\tCalibrate Sensors\n\
    2.\tSystem & Network Status\n\
    3.\tMotor Control and Tests\n\
    4.\tStart the Bioreactor\n>> '))

    return user_selection
    
def Run():
    '''Checks main menu and the resulting user input.'''
    
    user_input = Print_Menu_Query()
    
    # Calibrate Sensors
    if user_input == '1':
        Taris.Calibrate_Sensors()
        Run()

    # System & Network Status
    elif user_input == '2':
        Taris.Run_Bioreactor()
        Run()

    # Motor Control and Tests
    elif user_input == '3':
        Taris.Run_PWM()
        Run()

    # Start the Bioreactor
    elif user_input == '4':
        Taris.Run_Bioreactor()
        Run()

    # Resets menu if input is not 1, 2, 3, or 4
    else:
        Print_Menu_Query()

time.sleep(2)

Taris = Setup_Bioreactor()

Run()
