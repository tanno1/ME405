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
        '''!@brief      Initialize and returns an object associated with a DC motor.
        '''
        pass

    def set_duty (self, duty):
        '''!@brief      set the PWM duty cycle for the DC motor
            @details

            @param
        '''
        pass
    
    def enable (self):
        '''!@brief      Enable one channel of the L6206
            @details
        '''
        pass

if __name__ == '__main__':
    # adjust the following to write a test program for the L6206 class

    # create a timer object to use for motor control
    tim_A = Timer(n, freq = 20_000)

    # create an L6206 driver object
    mot_A = L6206(tim_A, pin.cpu.xx, pin.cpu.yy)

    # enable the L6206 driver
    mot_A.enable()

    mot_A.set_duty(40)
