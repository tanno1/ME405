# -*- coding: utf-8 -*-
"""
Homework 0x01: Reading CSV Files and Using matplotlib

Created on Sat Oct 14 21:56:08 2023

@author: kozyt
"""

"""
Explanation

string functions:
strip() removes any spaces
split(',') splits string into a list

file functions:
open() opens file
readline() returns a line from the file 

try and except: try tests program for errors, except lets program continue if ValueError 
"""

from matplotlib import pyplot

x_values = []
y_values = []

file = open('data.csv', mode = 'r')


header = file.readline().strip().split(',')

for line in file:
    data = line.strip().split(',')
    try:
        x = float(data[0])
        y = float(data[1])
        x_values.append(x)
        y_values.append(y)
    except ValueError:
        continue
    
pyplot.plot(x_values, y_values, marker = 'o')
pyplot.xlabel(header[0])
pyplot.ylabel(header[1])
pyplot.title(header[1]+" Vs. "+ header[0])
pyplot.grid(True)
pyplot.show()