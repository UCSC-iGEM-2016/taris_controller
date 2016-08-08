import Adafruit_ADS1x15

class Taris_ADC():

    def __init__(self,adc_address,i2c_bus):

        self.i2c_bus = i2c_bus
        self.adc_address = adc_address

    def setupADC(self):
        # Configure ADC for Adafruit's ADS1115 chip
        #print "ADS1115@:" + str(self.adc_address)
        self.adc = Adafruit_ADS1x15.ADS1115(address=self.adc_address, busnum=self.i2c_bus)
        return self.adc

    def readADC(self,adc_pin_address, adc_gain):
        return self.adc.read_adc(adc_pin_address, adc_gain)
