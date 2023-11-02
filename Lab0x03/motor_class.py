# Noah Tanner, Kosimo Tonn
# Lab 0x01: Driving DC Motors
# ME 405 - Professor Refvem
# Fall 2023

# imports
from pyb import Pin, Timer

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
        else:
            self.PWM1.pulse_width_percent(0)
            self.PWM2.pulse_width_percent(0)
    
    def enable (self):
        self.EN.high()
    
    def disable (self):
        self.EN.low()

# motor a
tim_A       = Timer(3, freq = 20_000)                               # timer3 for motor A
EN_a        = Pin(Pin.cpu.A10, mode=Pin.OUT_PP)                     # motA active high-enable
IN1_a       = Pin(Pin.cpu.B4, mode=Pin.OUT_PP)                      # motA control pin 1
IN2_a       = Pin(Pin.cpu.B5, mode=Pin.OUT_PP)                      # motA control pin 2
mot_A       = L6206(tim_A, EN_a, IN1_a, IN2_a)                      # initialize motor A object

# motor b
tim_B       = Timer(2, freq = 20_000)                               # timer2 for motor B
EN_b        = Pin(Pin.cpu.C1, mode=Pin.OUT_PP)                      # motB active high-enable
IN1_b       = Pin(Pin.cpu.A0, mode=Pin.OUT_PP)                      # motB control pin 1
IN2_b       = Pin(Pin.cpu.A1, mode=Pin.OUT_PP)                      # motB control pin 2
mot_B       = L6206(tim_B, EN_b, IN1_b, IN2_b)                      # initialize motor B object