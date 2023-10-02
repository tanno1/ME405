"""
Created on Thu Sep 28 14:42:03 2023

@author: Noah Tanner, Kozy Tonn
ME405 - Refvem
Lab 0x00 - Serial Communication and ADC Reading


"""

# imports
import pyb
from pyb import Pin, Timer, ADC, ExtInt
from time import sleep_ms   
from array import array

# pin configuration
PC1 = Pin(Pin.cpu.C1, mode=Pin.OUT_PP)
PC1.low()
PC0 = Pin(Pin.cpu.C0)
adc = pyb.ADC(PC0)
PA5 = Pin(Pin.cpu.A5, mode=Pin.OUT_PP)


data = array('H', 2500 * [0])  # Initialize an array of unsigned shorts (2 bytes each) with 1000 zeros.
idx = 0

# timer, trigger callbacks @ 1KHz w/ pyb.Timer class (timer 6, 7)
tim7 = Timer(7, freq = 1000)

def tim_cb(tim7):
    global data, idx
    if idx == 2500:
        tim7.callback(None)
    else:
        data[idx] = adc.read()
        idx += 1

def collect_data():
    PC1.high() # turn PC1 high
    tim7.callback(tim_cb)
    sleep_ms(2500)
    print("Type print_data() to print the new data")
    PC1.low()
    idx = 0

print("Type collect_data() to begin data collection")

def print_data():
    for i in range(0, 2500):
        print(f"{i}, {data[i]}")
    print("Type collect_data() to collect new data")
