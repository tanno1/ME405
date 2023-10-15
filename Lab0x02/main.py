'''!@file                       main.py
    @brief                      main file for lab0x02 in me405
    @details                    cal poly, san luis obispo me405 lab project
    @author                     noah tanner, kosimo tonn
    @date                       october, 2023
'''
# imports
from pyb import Pin, Timer
import time

class Encoder():
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
        self.delta = 0          # initialize delta as 0 for first pass
        self.position = 0       # initialize position as 0 for first pass

    def update(self):
        '''!@brief              updates encoder position and delta
            @details
        '''
        current_count = self.timer.count()
        self.delta = current_count - self.delta

        # check for underflow
        if self.delta > (self.ar / 2):
            delta -= ( self.ar + 1 )
        # check for overflow
        elif self.delta < (- ( self.ar + 1 ) / 2):
            delta += ( self.ar + 1 )

        # add delta to position (total movement that does not reset for each rev)
        self.position += delta

        # update delta to check each time
        prev_delta = delta

    def get_position(self):
        '''!@brief              gets the most recent encoder position
            @details
            @return
        '''
        pass

    def get_delta(self):
        '''!@brief              gets the most recent encoder delta
            @details
            @return
        '''
        pass

    def zero(self):
        '''!@brief              resets the encoder position to zero
            @details
        '''
        pass

if __name__ == "__main__":

    # config variables
    ps = 0
    ar = 65535
    ch_a_pin = Pin(Pin.cpu.B6, mode=Pin.OUT_PP)
    ch_b_pin = Pin(Pin.cpu.B7, mode=Pin.OUT_PP)
    
    # configure timer for encoder counter
    tim_2 = Timer(4, period = ar, prescaler = ps)
    tim_2.channel(1, pin=ch_a_pin, mode=Timer.ENC_AB) #Timer.ENC_AB configures timer in encoder mode, counter changes when ch1 OR ch2 changes
    tim_2.channel(2, pin=ch_b_pin, mode=Timer.ENC_AB)

    # check the number of elapsed ticks with counter() method of timer obj
    while True:
        count = tim_2.counter()
        time.sleep_ms(1000)
        print(count)
        