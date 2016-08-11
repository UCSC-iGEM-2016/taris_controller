
                               . =MM~ .                                         
                               .. =Z...                                         
                       ...      . .I8...                                        
                       . .       . Z+7..                                        
                       Z...   ......Z?I...                                      
                       +NMN=.........$Z?..                                      
                       . .,M?7?.......+MI:                                      
                            .$MZ+O=...,.M+78.   ..  .                           
                           .....?MM78O?+IM+++MMMMMMM.                           
                              ..,MD+++++?M++?MMMOM....                          
                          ..  ..+++==?NMIZM$++++++N...                          
                        . .IMMMMOO8MMM+++++++++++=+M..                          
                      ~NMMM.$$=MNMMMMM++++++++++++++M.  .                       
                    ..MMMMMMMMMMMMMMMM+++++++++++++++M . .                      
                       MMMD=IMMMMMMM7I+++++++++++++++$O...                      
                       .ZM++++I++++=+++I++++++++++++++M, .                      
                       .$++++++++++++7M+++++++++++++++IM.                       
                   .   8++++++++++++?M+++++++++++++++++DM.                      
                   ...I++++++++++++7M?++++++++++++++++O+M$                      
                   ...O+++++++++++MMM+7+++++++++++++++Z+IM+...                  
                   ..?I+++++++++DMZ+++M+++++++++++++++ZD+OM,..                  
                   ..7D++++++7M?+?ODNDZ+++++++++++++++++Z+MM..                  
                   .. .?O7MMMN?....  ..?MM+++++++++++++++I+OM. ...              
                   ..  ........ . . .  ...MD++++++++++++++++MM,..               
                                          .~M++++++++++++++++MM:.  ..           
                                          ...N++++++++++++++++NM=. .            
                                          ...,8+++++++++++++++++MM...           
                   ....  M . .               .D++++++++++++++++++NM...          
                    M ...7  +:              . =?++++++++++++++++++8M..          
                    ..:~.. =$             . . ,$+++++++++++++++++++IM.. ..      
               ...7.OMDZM8  . .. .        .   =I++++++++++++++++++++?M:...      
                 :MMMMMM:OM. .. + .        ...M+++++++++++++++++++++++ON..      
               . DMM.MMMM+MM...Z. ....=~Z+:$.M+++++++++++++++++++++++++7M..  .  
                MMMMMMMMMMZMM .. . .=7I...:88+++++++++?+++++++++++++++++?M . .  
               =MMMMMMMMMM8D8M. ...MM==+++++++++++++++$++++++++++++++++++IM...  
                .IMMMMMMMMMNDNM...DI7IIIII$O,7+++++=$8Z8+++++++++++++++++++M..  
                ..:MN.=MMMMM$87N. DMZ=NI.~MZNMZI++MD7+=++++++++++++++++++++IM.  
                  .~MMMI MMMM~=M= :8M=..M+++++++$+++++++++++++++++++++++++++DZ .
                . ..MMMM$.:MMM,ZM. .   .++++++?N8?$MMDZ?=+++I+++++++++++++++=M..
                     MMMMMMMDMM.MM.  . N+M$III77ZI8MD8M7+++++++++++++++++++++$D 
                   . .MMMMMMMMMMOMMZ:+$MMMMMM++++=++++++++++++++++++++++++++++M.
                    =NMMMMMMMMMM.MM8=DNMMMMMMMMMMMN+++++++++++++++++++++++++++M:
           .....:O7+++++++++++++=78M8MMMMMMMMMMMMMM+++++++++++++++++++++++++++N=
           ...M?+++++++++++++++++++++=+8MMMNI+++++++++++++++++++++++++++++++++D7
       ....~Z+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++M+
        ..=$++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++M,
       ..ZM++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++7M.
   .. .?++M++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++MD 
   ...D+++NN++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=D++++OM .
   ..:D++++MM+++++++++++++++++++++++++++++++++++++++++++++++++++++++++7++++IM:  
   ..O$+++++DM8++++++++++++++++++++++++++++++++++++++++++++++++++++++M+++++M?.  
   ..M8++++++?MMO+++++++8M$7I+++++++++++++++++++++++++++++++++++++++8++++7MI..  
   ..MZM++++++++DMMO++++$MMMMMMMM$8MO?I8ZONMO=+++++++++++++=++++++M+++++MM. .   
   ..O$+8$+++++++++8MZIIIIIIIII7IIIIIII7IIZMM+IO8N?++++++++++8$$MD+++$MM......  
  ...,M=+++?N++++++++MMIIIIIIIIIIIIIIIIIIIIIIZNNMD+7ONI++=++MMMO+++NMM:.        
 . ...8M++++ZZ=+N7++++OMZIIIIIIIIIIIIIIIIIIIIIIIIIINMMD+?NNNIZ8+=8MM..  ..      
.$MMMMZZM?++++++N?$+++++MMMMMMM8$IIIIIIIIIIIIIIIIIIIII?MZ+++++++N7+MI..  .      
MMMMMDI??+$ZNNO++?M7+++++M~.   ...........:+INMDZ7III$OODDMMIION+$Z$+++MMMMZ .  
...............NM+++$7+++OO .  ....................=II?=~:, :~~....:I8O7+~~I..  
               ..8N7+M+++OO                                                     
               .....N7OM+M.                                                     
               ......+NN7..

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
    server_address = "http://128.114.62.72:5000" # soe server
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
