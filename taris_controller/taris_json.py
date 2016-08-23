#!/usr/bin/python

from __future__ import print_function    # reconciles printing between python2 and python3
import io                                # used to create file streams
import urllib                            # pulling and requests
import json                              # used to format JSON from a dictionary
from datetime import datetime            # fetches the date and time
import requests

class Taris_JSON():
    
    def __init__(self, server_ip, server_post_path, server_pull_path):
        self.server_ip           = server_ip
        self.server_post_path    = server_post_path
        self.server_pull_path    = server_pull_path
        self.data = {}
        self.paramdata = {}
            
    def make_JSON(self, pH, temp, inPWM, outPWM, naohPWM, filtPWM, heaterPWM, inCURRENT, outCURRENT, naohCURRENT, filtCURRENT, des_pH, des_temp):

        pi_time = str(datetime.now())
        
        self.data = {
          'comment': 'This JSON is automatically sent with the most recent sensor/motor information to be read into the server side database.',
          'header': {
            'fromPItoServer_getSensorData': True,
            'date': pi_time
          },
          'payload': {
            'pH': pH,
            'temp': temp,
            'inMotor': {
              'PWM': inPWM,
              'current': inCURRENT
            },
            'outMotor': {
              'PWM': outPWM,
              'current': outCURRENT
            },
            'naohMotor': {
              'PWM': naohPWM,
              'current': naohCURRENT
            },
            'filterMotor': {
              'PWM': filtPWM,
              'current': filtCURRENT
            },
            'heater': {
              'PWM': heaterPWM
            },
            'parameters':{
               'des_pH': des_pH,
               'des_temp': des_temp
            }
          }
        }

    def make_param_JSON(self, sendTF, date_value, pH_value, temp_value, username):
        self.paramdata = {
          'comment': 'This JSON sends information back to the Pi from the server to give it new commands.',
          'header': {
            'toPIfromServer_sendSensorParams': sendTF,
            'date': date_value
          },
          'payload': {
            'des_pH': pH_value,
            'des_temp': temp_value,
            'user_changing': username
          }
        }

    def post_JSON(self):
        post_path = self.server_ip + self.server_post_path
        try:
            requests.post(post_path, json=json.dumps(self.data, indent=4))
        except:
            print('Error posting.')
            pass

    def pull_JSON(self):
        pull_path = self.server_ip + self.server_pull_path
        try:
            #response = urllib.urlopen(pull_path)
            #self.paramdata = json.loads(response.read())
            requests.pull(pull_path, json=self.paramdata)
        except:
            print('\nError pulling.')
            pass

###TRY requests.get(pull_path, json=json.load(self.paramdata, indent=4))
#        with open('strings.json') as json_data:
#        d = json.load(json_data)
#        print(d)
                
    def get_params(self):
        return False
