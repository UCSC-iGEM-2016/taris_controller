#!/usr/bin/python

from __future__ import print_function    # reconciles printing between python2 and python3
import io                                # used to create file streams
import json                              # used to format JSON from a dictionary
from datetime import datetime            # fetches the date and time
import requests

class Taris_JSON():
    
    def __init__(self, server_ip, server_post_path, server_pull_path):
        self.server_ip           = server_ip
        self.server_post_path    = server_post_path
        self.server_pull_path    = server_pull_path
        self.data = {}
            
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

    def post_JSON(self):
        path = self.server_ip + self.server_post_path
        try:
            requests.post(path, json=json.dumps(self.data, indent=4))
        except:
            print('Error posting.')
            pass
                
    def get_params(self):
        return False
