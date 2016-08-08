#!/usr/bin/python

from __future__ import print_function    # reconciles printing between python2 and python3
import io                                # used to create file streams
import fcntl                             # used to access I2C parameters like addresses
import time                              # used for sleep delay and timestamps
import json                              # used to format JSON from a dictionary
from datetime import datetime            # fetches the date and time

class Taris_JSON():

    #filename = 'example.json'

    def make_a_dic(pH, temp, inPWM, outPWM, naohPWM, filtPWM, inCURRENT, outCURRENT, naohCURRENT, filtCURRENT, des_pH, des_temp):
        pi_time = str(datetime.now())
        data_dic = {
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
        return(data_dic)

git remote add github git@github.com:/Some-Awesome-Project

    def make_JSON(data_dic, filename):
            try:
                    jsonfile = json.dumps(data_dic, indent=4)
                    f = open(filename, 'w')
                    f.write(jsonfile)
                    f.close()
            except:
                    print('ERROR opening: '), filename
                    pass

    #data_dics = make_a_dic(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    #make_JSONput(data_dics, filename)
