# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 12:59:17 2023

@author: kozyt
"""

from pyb import Pin, ADC
import time

class QTR_Sensor:
    def __init__(self):
        '''!@brief              creates a QTR sensor object
            @details            intializes the pins for adc
            @param
        '''
        
        # from calibration data
        self.line_detected_value = 1234
        
        # setup sensor pins
        P3          = Pin(Pin.cpu.A0, mode=Pin.IN)
        P4          = Pin(Pin.cpu.A1, mode=Pin.IN)
        P5          = Pin(Pin.cpu.A4, mode=Pin.IN)
        P6          = Pin(Pin.cpu.B0, mode=Pin.IN)
        P7          = Pin(Pin.cpu.A5, mode=Pin.IN)
        P8          = Pin(Pin.cpu.A6, mode=Pin.IN)
        P9          = Pin(Pin.cpu.A7, mode=Pin.IN)

        # adc setup
        self.adc3        = ADC(P3)
        self.adc4        = ADC(P4)
        self.adc5        = ADC(P5)
        self.adc6        = ADC(P6)
        self.adc7        = ADC(P7)
        self.adc8        = ADC(P8)
        self.adc9        = ADC(P9)
    
    def read_sensor(self):
        '''!@brief              reads from the sensor
            @details            returns values from proximity sensor
            @param
        '''
        sensor_values = [int(self.adc3.read()), 
                         int(self.adc4.read()),
                         int(self.adc5.read()),
                         int(self.adc6.read()),
                         int(self.adc7.read()),
                         int(self.adc8.read()),
                         int(self.adc9.read())]
        
        #time.sleep_ms(0.01) #sleep for 1 microsecond
        
        #for i in range(len(sensor_values)):
        #        if sensor_values[i] >= self.line_detected_value:
        #            sensor_values[i] = 1
        #        else:
        #            sensor_values[i] = 0
                    
        print(sensor_values)

### from calibration determine where the 1s and 0s are for motor adjustment code
if __name__ == '__main__':
    sensor = QTR_Sensor()   
    sensor.read_sensor()

    




