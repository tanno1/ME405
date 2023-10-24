# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 12:56:15 2023

@author: kozyt
"""

from matplotlib import pyplot
import serial

t_values = []
x_values = []
v_values = []

header1 = "Time (s)"
header2 = "Encoder Position (Ticks)"
header3 = "Velocity (RPM)"

data = serial.Serial('COM3', baudrate= 115600)

try:
    while True:
        line = data.readline().decode().strip().split(',')
        
        try:
            t = float(data[0])
            x = float(data[1])
            v = float(data[1])
            t_values.append(t)
            x_values.append(x)
            v_values.append(v)
            
        except ValueError:
            continue
        
except KeyboardInterrupt:
    pass

def PosPlot():
    pyplot.plot(t_values, x_values)
    pyplot.xlabel(header1)
    pyplot.ylabel(header2)
    pyplot.title(header2 +" Vs. "+ header1)
    pyplot.grid(True)
    pyplot.show()
    
def VeloPlot():
    pyplot.plot(t_values, v_values)
    pyplot.xlabel(header1)
    pyplot.ylabel(header3)
    pyplot.title(header3 +" Vs. "+ header1)
    pyplot.grid(True)
    pyplot.show()