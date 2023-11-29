'''
    @name                  lab4_main.py
    @brief                 lab4 main file for circle line following
    @author                tanner, noah
    @date                  november, 2023
'''

from pyb import Pin, ADC
import romi_driver as driver
import time

# sensor array [ 3, 4, 5, 6, 7, 8, 9 ] with 3 being on left when romi faces forward

# setup sensor pins
P3          = Pin(Pin.cpu.A0, mode=Pin.IN)
P4          = Pin(Pin.cpu.A1, mode=Pin.IN)
P5          = Pin(Pin.cpu.A4, mode=Pin.IN)
P6          = Pin(Pin.cpu.B0, mode=Pin.IN)
P7          = Pin(Pin.cpu.A5, mode=Pin.IN)
P8          = Pin(Pin.cpu.A2, mode=Pin.IN)
P9          = Pin(Pin.cpu.A3, mode=Pin.IN)

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

# calibration values:
white = [314.3, 308.7, 304.7, 300.3, 294.1, 1937.8, 3586.8]
black = [2542.8, 2409.3, 2263.4, 2119.5, 2029.3, 1956.1, 3576.0]

def calibrate(color):
    cal_array   = [ 0, 0, 0, 0, 0, 0, 0 ]
    idx         = 0
    iter        = 10

    if color == 'white':
        while iter > 0:
            while idx < len(cal_array):
                cal_array[idx] += adc_array[idx].read()
                idx += 1
            time.sleep(1)
            idx = 0
            iter -= 1
            print(cal_array)

        white_cal_array = [ ( val / 10 ) for val in cal_array ]
        return white_cal_array

    if color == 'black':
        while iter > 0:
            while idx < len(cal_array):
                cal_array[idx] += adc_array[idx].read()
                idx += 1
            time.sleep(1)
            idx = 0
            iter -= 1
            print(cal_array)

        black_cal_array = [ ( val / 10 ) for val in cal_array ]
        return black_cal_array

def straight():
    pass

def right():
    pass

def left():
    pass

def stop():
    pass

if __name__ == '__main__':

    # left driver
    left = driver.romi_driver

    # right driver
    right = driver.romi_driver()

# read function
# while True:
#     idx = 0
#     for idx in range(0, 7):
#         val_array[idx] = adc_array[idx].read()
#         idx += 1
#     print(val_array)
#     time.sleep(1.25)


