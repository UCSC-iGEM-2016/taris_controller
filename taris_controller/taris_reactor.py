from taris_adc import Taris_ADC as ADC
from taris_sensor import Taris_Sensor as Sensor
from taris_pid import PID
from taris_json import Taris_JSON as IOX
import os
import time

class Taris_Reactor():
    '''Holds the object that runs the bioreactor and handles data aggregation. \
    Requires the Atlas Scientific EZO pH and RTD sensor objects, and the \
    Texas Instruments ADS1115 analog to digital converter object (uses the \
    Adafruit ADS1x15 library.'''

    def __init__(self,
                  adc_address,          \
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
                  server_pull_path):

        # Instantiate ADC (ADS1115) object
        self.ads           = ADC(adc_address, i2c_bus)
        self.ads.setupADC() 
        
        # Instantiate atlas objects
        self.temp_sensor   = Sensor(temp_sensor_address,i2c_bus)
        self.pH_sensor     = Sensor(pH_sensor_address,i2c_bus)
        self.adc_gain      = adc_gain
        
        # Network Handler
        
        self.JSON_Handler = IOX(server_ip, server_post_path, server_pull_path)
        
        #Set RTD Sensor unit and verify        
        print("Setting RTD sensor to Celsius...")
        temp_unit = "C" # F,C, or K
        self.temp_sensor.write("S," + temp_unit + "\0x0d") # Set sensor to Celsius
        q = self.temp_sensor.query("S,?\0x0d")
        
        if str(q) == "?S,"+temp_unit:
            print("RTD set: " + str(q))
        else:
            print("Error setting RTD sensor unit: " + str(q))
        
        self.pH_sensor.verify()
        self.temp_sensor.verify()
        
        
        # Clear EZO pH and RTD internal data
        self.temp_sensor.write("M,CLEAR")
        
         # Internal data
        self.current_pH      = 0
        self.current_temp    = 0
        
        self.inflow_PWM      = 0
        self.outflow_PWM     = 0
        self.naoh_PWM        = 0
        self.filter_PWM      = 0
        self.heater_PWM      = 0
        
        self.inflow_i        = 0
        self.outflow_i       = 0
        self.naoh_i          = 0
        self.filter_i        = 0
        
        self.des_pH          = 0
        self.des_temp        = 0
        
        self.inflow_rate     = 0
        self.outflow_rate    = 0
        self.filter_rate     = 0
        
        # ADS pin settings        
        
        self.inflow_ads_pin  = inflow_ads_pin
        self.outflow_ads_pin = outflow_ads_pin
        self.naoh_ads_pin    = naoh_ads_pin
        self.filter_ads_pin  = filter_ads_pin
        
        # PID parameters

        self.pwm_frequency   = pwm_frequency
        self.sample_frequency= sample_frequency
        self.sample_time     = 1.0 / self.sample_frequency
        self.pH_def          = pH_def
        self.temp_def        = temp_def
        self.temp_output     = 0
        self.pH_output       = 0
        self.temp_error_prev = 0
        self.temp_int_prev   = 0
        self.pH_error_prev   = 0
        self.pH_int_prev     = 0
        
        # Control parameters
        
        self.stop_reactor    = False
        self.time_count      = 0
        
    def cls(self):
        '''Clears the terminal.'''
        os.system('cls' if os.name=='nt' else 'clear')

    def Calibrate_Sensors(self):
        '''UI for sensor calibration selection.'''
        self.cls()
        user_selection = str(input("Please select from the options below:\n\
            1.\tCalibrate pH sensor\n\
            2.\tCalibrate temp sensor\n\
            3.\tCalibrate both temp and pH. Temperature will be used\n\
            \tfor additional pH calibration.\n>>"))
        if user_selection == '1':
            self.pH_sensor.pH_calibrateSensor()
        elif user_selection == '2':
            self.temp_sensor.temp_calibrateSensor()
        elif user_selection == '3':
            self.pH_sensor.pH_calibrateSensor()
            self.temp_sensor.temp_calibrateSensor()
            setup_temp = self.temp_sensor.getData()
            self.pH_sensor.pH_compensateTemp(setup_temp)

    def Display_Status(self):
        '''Displays relevant information while reactor is running.'''
               
        self.cls()
        
        status_message = 'Taris V1.0 Bioreactor | Current time:' + str(time.strftime("%d-%m-%Y @ %H:%M:%S")) + '\n' +\
            'Temp:   '     + str(self.current_temp)     + '\n' +\
            'pH:     '     + str(self.current_pH)       + '\n' +\
            'Inflow: '     + str(self.inflow_i)         + '\n' +\
            'Outflow:'     + str(self.outflow_i)        + '\n' +\
            'NaOH:   '     + str(self.naoh_i)           + '\n' +\
            'Filter: '     + str(self.filter_i)         + '\n'

        print(status_message)
        
        # Make a new JSON and post to the server
        self.JSON_Handler.make_JSON(self.current_pH,  \
                   self.current_temp,\
                   self.inflow_PWM,  \
                   self.outflow_PWM, \
                   self.naoh_PWM,    \
                   self.filter_PWM,  \
                   self.heater_PWM,  \
                   self.inflow_i,    \
                   self.outflow_i,   \
                   self.naoh_i,      \
                   self.filter_i,    \
                   self.des_pH,      \
                   self.des_temp)
        self.JSON_Handler.post_JSON()

    def Sample_Bioreactor(self):
        '''Gets data from bioreactor sensors.'''

        # Get sensor values
        self.Check_Sensors()
        
        # Update PWM
        self.Query_Motor_PWM()        
        
        # Get motor currents
        self.Query_Motor_Current()

    def Run_Bioreactor(self):
        '''Runs the bioreactor sampler at 1Hz.'''

        while self.stop_reactor==False:
            # Get updated values and run control

            self.Sample_Bioreactor()

            # Display current values

            self.Display_Status()
            
            time.sleep(1)


    def Check_Sensors(self):
        '''Gets current pH and temp from the EZO pH and RTD sensors.'''
        self.current_pH = self.pH_sensor.getData()
        self.current_temp = self.temp_sensor.getData()
        
    def V_to_I(self,voltage):
        '''Converts ADS1115 voltage reading to a current, since the value \
        at each of its pins measure the drop across a current sensor resistor \
        respective to each motor.'''
        
        res = 0.1
        return int(voltage)/res
        
    def Flowrate_to_PWM(self,input_rate):
        '''Converts desired flowrate to a PWM value.'''
        converted_value = 0.0431*input_rate - 0.5509
        return converted_value
    
    def Query_Motor_PWM(self):
        # Run a PID on the temperature and update PWM

        self.heater_PWM, self.temp_error_prev, self.temp_int_prev = PID(self.current_temp, \
                                                      self.temp_def,     \
                                                      self.sample_time,  \
                                                      self.temp_int_prev,\
                                                      self.temp_error_prev)
        # Run a PID on the pH and update PWM

        self.naoh_PWM, self.pH_error_prev, self.pH_int_prev = PID(self.current_pH, \
                                                self.pH_def,     \
                                                self.sample_time,\
                                                self.pH_int_prev,\
                                                self.pH_error_prev)

    def Query_Motor_Current(self):
        '''Returns the current flowing through each motor by measuring the \
        voltage drop across a current sense resistor.'''
        self.inflow_i  = self.V_to_I(self.ads.readADC(self.inflow_ads_pin,self.adc_gain))
        self.outflow_i = self.V_to_I(self.ads.readADC(self.outflow_ads_pin,self.adc_gain))
        self.naoh_i    = self.V_to_I(self.ads.readADC(self.naoh_ads_pin,self.adc_gain))
        self.filt_i    = self.V_to_I(self.ads.readADC(self.filter_ads_pin,self.adc_gain))
