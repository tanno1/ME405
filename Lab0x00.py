#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 14:42:03 2023

@author: Noah Tanner, Kozy Tonn

ME405 - Refvem
Lab 0x00 - Serial Communication and ADC Reading


"""

# imports
from pyb import Pin, Timer, ADC
from array import array
from time import sleep_ms


# main

# pin configuration
PC1 = Pin(Pin.cpu.C1, mode=Pin.OUT_PP)
PC0 = Pin(Pin.cpu.C0)
ADC = ADC(PC0)
    # to read... val = ADC.read()!
    
# timer, trigger callbacks @ 1KHz w/ pyb.Timer class (timer 6, 7)

def tim_cb(tim):
    global data, idx
    #f(n) code here!

tim7 = Timer(7, freq = 1000)
tim7.callback(tim_cb)
    # to turn off callback -> tim7.callback(None)