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

    def __init__ (self, PWM_tim, IN1_pin, IN2_pin):
        self.tim = PWM_tim
        self.PWM1 = self.tim.channel(1, mode=Timer.PWM)
        self.PWM2 = self.tim.channel(2, mode=Timer.PWM)
        self.EN = EN_pin

    def set_duty (self, duty):

        "add logic"
        self.PWM_1.pulse_width_percent(duty)
        self.PWM_2.pulse_width_percent(0)
        
        self.PWM_1.pulse_width_percent(0)
        self.PWM_2.pulse_width_percent(-1*duty)
        '''!@brief      set the PWM duty cycle for the DC motor
            @details

            @param
        '''
        pass
    
    def enable (self):

        self.EN.high()
        pass
        

if __name__ == '__main__':
    # uncomment and use with forward() to run one motor for testing
    #
    #EN1 = Pin(Pin.cpu.A10, mode=Pin.OUT_PP) # active-high enable pin
    #IN1 = Pin(Pin.cpu.B4, mode=Pin.OUT_PP) # control pin 1
    #IN2 = Pin(Pin.cpu.B5, mode=Pin.OUT_PP) # control pin 2

    # set forward
    def forward(EN1, IN1, IN2):
        EN1.high()
        IN1.high()
        IN2.low()


    # adjust the following to write a test program for the L6206 class

    # create a timer object to use for motor control
    #tim_A = Timer(n, freq = 20_000)

    # create an L6206 driver object
    #mot_A = L6206(tim_A, Pin.cpu.xx, Pin.cpu.yy)
    #mot_B = L6206(tim_A, Pin.cpu.xx, Pin.cpu.yy)

    # enable the L6206 driver
    #mot_A.enable()

    #mot_A.set_duty(40)
