# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 12:21:37 2023

@author: kozyt
"""


from pyb import UART

class UART_connection:
    
    def __init__(self):
        #init
        self.uart = UART(2, 115200)                         # init with given baudrate
        self.uart.init(115200, bits=8, parity=None, stop=1) # init with given parameters

    def run(self, data):
        #Writes Data
        self.uart.write(str(data))
    
    def off(self):
        #Shuts Off UART Connection
        self.uart.deinit()

