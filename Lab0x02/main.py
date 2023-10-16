'''!@file                       main.py
    @brief                      main file for lab0x02 in me405
    @details                    cal poly, san luis obispo me405 lab project
    @author                     noah tanner, kosimo tonn
    @date                       october, 2023
'''
# imports
import motor_class_main
from pyb import Pin, Timer
from array import array
import time

class collector:
    '''!@brief
        @details
    '''
    
    def __init__(self, tim, encoder):
        '''!@brief              creates a collector object
            @details
            @param
        '''
        self.tim            = tim
        self.encoder        = encoder
        self.total_position = array( 'L', [0 for n in range(1000)]) 
        self.time           = array( 'L', [0 for n in range(1000)]) 
        self.delta          = array( 'L', [0 for n in range(1000)]) 
        self.idx            = 0
    
    def start(self, motor, duty_cycle):
        # initialize timer callback
        self.tim.callback(self.tim_cb)
    
    def tim_cb(self, cb_src):
        '''!@brief              timer callback for encoder
            @details
        '''
        # add total position, time, and delta values to respective arrays
        self.total_position[self.idx] = self.encoder.get_position()
        self.time[self.idx]           = time.ticks_diff()
        self.delta[self.idx]          = self.encoder.get_delta()
        
        # increment array index 
        self.idx += 1

class Encoder:
    '''!@brief                  interface with quadrature encoders
        @details
    '''
    def __init__(self, timer, cha, chb, ar, ps):
        '''!@brief              creates an encoder object
            @details
            @param
        '''
        self.callback = None
        self.timer = timer
        self.cha = cha
        self.chb = chb
        self.ar = ar
        self.ps = ps
        self.prev_delta = 0             # initialize previous delta
        self.current_delta = 0          # initialize delta as 0 for first pass
        self.total_position = 0         # initialize total position as 0 for first pass
        self.prev_position = 0          # initialize previous position as 0 for first pass
        self.current_position = 0       # initialize the current position as 0 for first pass

        # to prevent MemoryException errors for repeat calculations:
        self.under_check = ( self.ar / 2 )
        self.over_check = ( -( self.ar + 1 )/2 )
        self.ar_add_1 = self.ar + 1

    def update(self):
        '''!@brief              updates encoder position and delta
            @details
            @param return
        '''
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

        # update delta to check each time
        self.prev_delta = self.current_delta

        # update previous position to current position
        self.prev_position = self.current_position

    def get_position(self):
        '''!@brief              gets the most recent encoder position
            @details
            @return
        '''
        return self.current_position

    def get_delta(self):
        '''!@brief              gets the most recent encoder delta
            @details
            @return
        '''
        return self.current_delta

    def zero(self):
        '''!@brief              resets the encoder position to zero
            @details
        '''
        self.total_position = 0
        self.current_position = 0
        print("Total encoder position reset to 0")

if __name__ == "__main__":

    # config variables
    ps = 0
    ar = 65535
    ch_a_pin = Pin(Pin.cpu.B6, mode=Pin.OUT_PP)
    ch_b_pin = Pin(Pin.cpu.B7, mode=Pin.OUT_PP)
    
    # configure timer for encoder counter
    tim_4 = Timer(4, period = ar, prescaler = ps)
    cha = tim_4.channel(1, pin=ch_a_pin, mode=Timer.ENC_AB) #Timer.ENC_AB configures timer in encoder mode, counter changes when ch1 OR ch2 changes
    chb = tim_4.channel(2, pin=ch_b_pin, mode=Timer.ENC_AB)

    # make encoder instance
    encoder_1 = Encoder(tim_4, cha, chb, ar, ps)

    # make collector instance, assign callback method
    collector_1 = collector(tim_4, encoder_1)

    while True:
        collector_1.tim_cb(tim_4)
        print(collector_1.time)


    

        