#!/usr/bin/python

from __future__ import print_function    # reconciles printing between python2 and python3
import io                                # used to create file streams
import fcntl                             # used to access I2C parameters like addresses
import json                              # used to format JSON from a dictionary
from datetime import datetime            # fetches the date and time
import requests

class Taris_JSON():
    
    def __init__(self, server_ip, server_post_urlpath, server_pull_urlpath):
        self.test = 0

    def post_JSON(self, jsonfile, server_post_urlpath)
        r = requests.post(server_post_urlpath, jsonfile)
        return(r.status_code) # returns status in the 200's if successful

    def make_dict(self, pH, temp, inPWM, outPWM, naohPWM, filtPWM, inCURRENT, outCURRENT, naohCURRENT, filtCURRENT, des_pH, des_temp):
        pi_time = str(datetime.now())
        data = {
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
            'parameters':{
               'des_pH': des_pH,
               'des_temp': des_temp
            }
          }
        }
        return(data)

    def create_JSON(self, data, filename):
            try:
                    jsonfile = json.dumps(data_dic, indent=4)
                    f = open(filename, 'w')
                    f.write(jsonfile)
                    f.close()
            except:
                    print('ERROR opening: '), filename
                    pass

    #filename = 'example.json'
    #data = make_dict(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    #create_JSON(data, filename)
