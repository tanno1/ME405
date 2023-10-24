'''!@file                       encoder_class.py
    @brief                      encoder/colelctor class, originally from lab0x02
    @details                    cal poly, san luis obispo me405 lab project
    @author                     noah tanner, kosimo tonn
    @date                       october, 2023
'''
# imports
from pyb import Pin, Timer
from array import array
import math

class collector:
    '''!@brief
        @details
    '''

    def __init__(self, tim, encoder, motor):
        '''!@brief              creates a collector object
            @details
            @param
        '''
        self.tim            = tim
        self.motor          = motor
        self.encoder        = encoder
        self.position       = array( 'L', [0 for n in range(1000)])      # short data set
        self.time           = array( 'L', [0 for n in range(1000)])      #
        self.delta          = array( 'L', [0 for n in range(1000)])      #
        self.long_position  = array( 'L', [0 for n in range(1)])     # long data set
        self.long_time      = array( 'L', [0 for n in range(1)])     #
        self.long_delta     = array( 'L', [0 for n in range(1)])     #
        self.idx            = 0
        self.start_time     = 0
        self.end_time       = 0
        self.type           = 0
    
    def start(self, duty_cycle, type):
        self.duty_cycle     = duty_cycle
        self.type           = type
        self.motor.enable()
        self.motor.set_duty(self.duty_cycle)
        self.tim.callback(self.tim_cb)
        if (self.idx == 999 and self.type == 1) or (self.idx == 29999 and self.type == 2):
            self.tim.callback(None)
    
    def tim_cb(self, tim):
        '''!@brief              timer callback for encoder
            @details
        '''
        # add total position, time, and delta values to respective arrays
        self.encoder.update()                                               # update encoder position
        # differentiate between short and long response recording
        if self.type == 1:
            self.position[self.idx]       = self.encoder.total_position
            self.delta[self.idx]          = self.encoder.current_delta
            self.time[self.idx]           = self.idx
        elif self.type == 2:
            self.long_position[self.idx]  = self.encoder.total_position
            self.long_delta[self.idx]     = self.encoder.current_delta
            self.long_time[self.idx]      = self.idx
        else:
            print('Invalid recording type, try again')
            self.type == 998
        self.idx += 1
        if (self.idx == 999 and self.type == 1) or (self.idx == 29999 and self.type == 2):
            self.tim.callback(None)
            self.motor.disable()

    def organize_data(self):
        print('Time', 'Position', 'Delta')
        for i in range(1000):
            print(f"{self.time[i]},{self.position[i]},{self.delta[i]}")

class Encoder:
    '''!@brief                  interface with quadrature encoders
        @details
    '''
    def __init__(self, timer, cha, chb, ar, ps):
        '''!@brief              creates an encoder object
            @details
            @param
        '''
        self.timer = timer
        self.cha = cha
        self.chb = chb
        self.ar = ar
        self.ps = ps
        self.current_delta          = 0               # initialize delta as 0 for first pass
        self.total_position         = 0               # initialize total position as 0 for first pass
        self.prev_position          = 0               # initialize previous position as 0 for first pass
        self.current_position       = 0               # initialize the current position as 0 for first pass
        self.velocity = {
                            'rad/s' :0, 
                            'rpm'   :0
                                        }             # initialize velocity as 0 

        # to prevent MemoryException errors for repeat calculations:
        self.under_check = ((self.ar+1)/2)
        self.over_check = (-1*( self.ar + 1 ))/2
        self.ar_add_1 = self.ar + 1

    def update(self):
        self.current_position = self.timer.counter()
        self.current_delta = self.current_position - self.prev_position

        # check for underflow
        if self.current_delta > self.under_check:
            self.current_delta -= self.ar_add_1

        # check for overflow
        elif self.current_delta < self.over_check:
            self.current_delta += self.ar_add_1

        # add delta to total position (total movement that does not reset for each rev)
        self.total_position += self.current_delta

        # update previous position to current position
        self.prev_position = self.current_position

    def vel_calc(self):
        # dictionary of velocity values in diff units
        self.velocity['rad/s']  = self.current_delta * 24.54
        self.velocity['rpm']    = self.velocity['rad/s'] / (2*math.pi)

        return self.velocity

    def get_position(self):
        return self.current_position

    def get_delta(self):
        return self.current_delta

    def zero(self):
        self.prev_delta         = 0             # initialize previous delta
        self.current_delta      = 0             # initialize delta as 0 for first pass
        self.total_position     = 0             # initialize total position as 0 for first pass
        self.prev_position      = 0             # initialize previous position as 0 for first pass
        self.current_position   = 0             # initialize the current position as 0 for first pass
