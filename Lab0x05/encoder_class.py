'''!@file                       encoder_class.py
    @brief                      encoder/colelctor class, originally from lab0x02
    @details                    cal poly, san luis obispo me405 lab project
    @author                     noah tanner, kosimo tonn
    @date                       october, 2023
'''
# imports
from pyb import Pin, Timer
import time
from array import array

class Encoder:
    '''!@brief                  interface with quadrature encoders
        @details
    '''
    def __init__(self, timer, cha, chb, ar, ps):
        '''!@brief              creates an encoder object
            @details
            @param
        '''
        self.timer                  = timer
        self.last_update            = time.ticks_us()
        self.cha                    = cha
        self.chb                    = chb
        self.ar                     = ar
        self.ps                     = ps
        self.current_delta          = 0                 # initialize delta as 0 for first pass
        self.total_position         = 0                 # initialize total position as 0 for first pass
        self.prev_position          = 0                 # initialize previous position as 0 for first pass
        self.current_position       = 0                 # initialize the current position as 0 for first pass
        self.velocity = {
                            'rad/s' :0, 
                            'rpm'   :0
                                        }             # initialize velocity as 0 

        # to prevent MemoryException errors for repeat calculations:
        self.under_check = ((self.ar)/2)
        self.over_check = (-1*( self.ar + 1 ))/2
        self.ar_add_1 = self.ar + 1

    def update(self):
        self.current_position   = self.timer.counter()
        self.current_delta      = self.current_position - self.prev_position
        # check for underflow
        if self.current_delta > self.under_check:
            self.current_delta -= self.ar_add_1
        # check for overflow
        elif self.current_delta < self.over_check:
            self.current_delta += self.ar_add_1
        # add delta to total position (total movement that does not reset for each rev)
        self.total_position += self.current_delta
        # update previous position to current position
        self.prev_position      = self.current_position

    def vel_calc(self, pos1, pos2, time_diff):
        # dictionary of velocity values in diff units
        delta = pos2 - pos1
        self.velocity['rad/s']  = delta / time_diff
        self.velocity['rpm']    = self.velocity['rad/s'] * 3.66

    def get_position(self):
        self.update()
        return self.current_position

    def get_delta(self):
        return self.current_delta

    def zero(self):
        self.prev_delta         = 0             # initialize previous delta
        self.current_delta      = 0             # initialize delta as 0 for first pass
        self.total_position     = 0             # initialize total position as 0 for first pass
        self.prev_position      = 0             # initialize previous position as 0 for first pass
        self.current_position   = 0             # initialize the current position as 0 for first pass
