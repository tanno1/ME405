'''
    @name                  lab4_main.py
    @brief                 lab4 main file for circle line following
    @author                tanner, noah
    @date                  november, 2023
'''

from pyb import Pin, ADC, Timer
import romi_driver as driver
import encoder_class as encoder
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
    tim_left        = Timer(4, freq = 20_000)
    pwm_left_pin    = Pin(Pin.cpu.B8, mode=Pin.OUT_PP)
    pwm_left        = tim_left.channel(3, pin = pwm_left_pin, mode=Timer.PWM)
    dir_left_pin    = Pin(Pin.cpu.B9, mode=Pin.OUT_PP)
    en_left_pin     = Pin(Pin.cpu.B7, mode=Pin.OUT_PP)
    left            = driver.romi_driver(tim_left, pwm_left, dir_left_pin, en_left_pin)

    # right driver
    tim_right       = Timer(8, freq = 20_000)
    pwm_right_pin   = Pin(Pin.cpu.C9)
    dir_right_pin   = Pin(Pin.cpu.C8, mode=Pin.OUT_PP)
    en_right_pin    = Pin(Pin.cpu.C7, mode=Pin.OUT_PP)
    # configure channels 2, 3, 4
    pwm_right       = tim_right.channel(4, pin = pwm_right_pin, mode=Timer.PWM)
    right           = driver.romi_driver(tim_right, pwm_right, dir_right_pin, en_right_pin)

    # encoder left
    ps          = 0
    ar          = 1000
    l_pin_cha   = Pin(Pin.cpu.B4, mode=Pin.OUT_PP)                          # encoder 1, channel a pin
    l_pin_chb   = Pin(Pin.cpu.B5, mode=Pin.OUT_PP)                          # encoder 1, channel b pin
    tim_left_3  = Timer(3, period = ar, prescaler = ps)                     # encoder 1 timer
    l_cha       = tim_left_3.channel(1, pin=l_pin_cha, mode=Timer.ENC_AB)  
    l_chb       = tim_left_3.channel(2, pin=l_pin_chb, mode=Timer.ENC_AB)  
    enc_right   = encoder.Encoder(tim_left_3, l_cha, l_chb, ar, ps)         # encoder 1 instance

    # # encoder right
    # r_pin_cha   = Pin(Pin.cpu.A8, mode=Pin.OUT_PP)                          # encoder 1, channel a pin
    # r_pin_chb   = Pin(Pin.cpu.A9, mode=Pin.OUT_PP)                          # encoder 1, channel b pin
    # tim_left_1  = Timer(1, period = ar, prescaler = ps)                     # encoder 1 timer
    # r_cha       = tim_left_1.channel(1, pin=r_pin_cha, mode=Timer.ENC_AB)  
    # r_chb       = tim_left_1.channel(2, pin=r_pin_chb, mode=Timer.ENC_AB)  
    # enc_left    = encoder.Encoder(tim_left_1, r_cha, r_chb, ar, ps)         # encoder 1 instance