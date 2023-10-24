# Noah Tanner, Kosimo Tonn
# Lab 0x01: Driving DC Motors
# ME 405 - Professor Refvem
# Fall 2023

# imports
from pyb import Pin, Timer

# class definitions

class L6206:
    '''!@brief      A driver class for one channel of the L2606
        @details    Objects of this class can be used to apply PWM to a given DC motor on one channel of the L6206 from ST Microelectronics.
    '''

    def __init__ (self, PWM_tim, EN_pin, IN1_pin, IN2_pin):
        self.tim = PWM_tim
        self.PWM1 = PWM_tim.channel(1, pin=IN1_pin, mode=Timer.PWM)
        self.PWM2 = PWM_tim.channel(2, pin=IN2_pin, mode=Timer.PWM)
        self.EN = EN_pin

    def set_duty (self, duty):
        '''!@brief      set the PWM duty cycle for the DC motor
            @details
            @param
        '''
        if duty >= 0:
            self.PWM1.pulse_width_percent(duty)
            self.PWM2.pulse_width_percent(0)
        elif duty <= 0:
            self.PWM1.pulse_width_percent(0)
            self.PWM2.pulse_width_percent(-1*duty)
        elif duty == 0:
            self.PWM1.pulse_width_percent(0)
            self.PWM2.pulse_width_percent(0)
    
    def enable (self):
        self.EN.high()
    
    def disable (self):
        self.EN.low()
