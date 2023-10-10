'''!@file                       main.py
    @brief                      main file for lab0x02 in me405
    @details                    cal poly, san luis obispo me405 lab project
    @author                     noah tanner, kosimo tonn
    @date                       october, 2023
'''
# imports
from pyb import Pin, Timer
import time

class Encoder:
    '''!@brief                  interface with quadrature encoders
        @details
    '''

    def __init(self):
        '''!@brief              creates an encoder object
            @details
            @param
        '''
        pass

    def update(self):
        '''!@brief              updates encoder position and delta
            @details
        '''
        pass

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
    ch_a_pin = Pin(Pin.cpu.A0, mode=Pin.OUT_PP)
    ch_b_pin = Pin(Pin.cpu.A1, mode=Pin.OUT_PP)
    
    # configure timer for encoder counter
    tim_2 = Timer(2, period = ar, prescaler = ps)
    tim_2.channel(1, pin=ch_a_pin, mode=Timer.ENC_AB) #Timer.ENC_AB configures timer in encoder mode, counter changes when ch1 OR ch2 changes
    tim_2.channel(2, pin=ch_b_pin, mode=Timer.ENC_AB)

    # check the number of elapsed ticks with counter() method of timer obj
    while True:
        count = tim_2.counter()
        time.sleep_ms(1000)
        print(count)