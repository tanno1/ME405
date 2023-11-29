'''
    @name                  lab4_main.py
    @brief                 lab4 main file for circle line following
    @author                tanner, noah
    @date                  november, 2023
'''

from pyb import pin, ADC
import time

# sensor array [ 3, 4, 5, 6, 7, 8, 9 ] with 3 being on left when romi faces forward

# setup sensor pins
P3          = Pin(Pin.cpu.A0, mode=Pin.IN)
P4          = Pin(Pin.cpu.A1, mode=Pin.IN)
P5          = Pin(Pin.cpu.A2, mode=Pin.IN)
P6          = Pin(Pin.cpu.A3, mode=Pin.IN)
P7          = Pin(Pin.cpu.D13, mode=Pin.IN)
P8          = Pin(Pin.cpu.D1, mode=Pin.IN)
P9          = Pin(Pin.cpu.D0, mode=Pin.IN)

# adc setup
adc3        = ADC(P3)
adc4        = ADC(P4)
adc5        = ADC(P5)
adc6        = ADC(P6)
adc7        = ADC(P7)
adc8        = ADC(P8)
adc9        = ADC(P9)

val_array   = [ 0, 0, 0, 0, 0, 0, 0 ]
adc_array   = [ adc3, adc4, adc5, adc6, adc7, adc8, adc9 ]

# read function
while True:
    idx = 0
    for idx in range(0, 7):
        val_array[idx] = adc_array[idx].read()
        idx += 1
    print(val_array)
    time.sleep(1.25)
