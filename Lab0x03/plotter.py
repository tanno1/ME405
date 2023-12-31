# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 12:56:15 2023

@author: kozyt
"""

from matplotlib import pyplot
import serial
import time
import math

pos_values  = []
time_values = []
vel_values  = []

header1 = "Time (s)"
header2 = "Encoder Position (Ticks)"
header3 = "Velocity (RPM)"

def PosPlot():
    pyplot.plot(time_values, pos_values)
    pyplot.xlabel(header1)
    pyplot.ylabel(header2)
    pyplot.title(header2 +" Vs. "+ header1)
    pyplot.grid(True)
    pyplot.show()
    
def VeloPlot():
    pyplot.plot(time_values, vel_values)
    pyplot.xlabel(header1)
    pyplot.ylabel(header3)
    pyplot.title(header3 +" Vs. "+ header1)
    pyplot.grid(True)
    pyplot.show()

data = serial.Serial('/dev/cu.usbmodem142303', baudrate= 115600)

def data_collect():
    noprint = 0
    stop    = False
    while not stop:
        try:
            if noprint == 0:
                line = data.readline().decode('utf-8', errors = 'replace').strip().split(',')
                split = str(line[0])
                split = split.split('\t')
                print(split)
            try: 
                pos = float(split[0])
                time = float(split[1])
                vel = float(split[2])
                pos_values.append(pos)
                time_values.append(time)
                if vel < 0:
                    vel_values.append(vel_values[-1])
                else:
                    vel_values.append(vel)
            except IndexError:
                print('Unicode Decode Error caused Indexing error, data point skipped')
        
        except UnicodeDecodeError:
            print('Unicode Decode Error')

        except ValueError:
            print('Value')

        except KeyboardInterrupt:            # exit collection
            print('Keyboard interrupt')
            PosPlot()                        # plot pos vs t
            VeloPlot()                       # plot vel vs t
            noprint = 1
            stop = True

def reset():
    global pos_values, time_values, vel_values
    pos_values      = []
    time_values     = []
    vel_values      = []

while True:
    print("Command choices:")
    print("1. data_collect()")
    print("2. reset()")
    choice = input("Enter a command number: ")

    if choice == "1":
        noprint = 0
        data_collect()
        print('Data collection vars reset')
        reset()
    elif choice == "2":
        reset()
    else:
        print("Invalid command, try again.")
