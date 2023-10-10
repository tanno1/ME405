'''!@file                       main.py
    @brief                      main file for lab0x02 in me405
    @details                    cal poly, san luis obispo me405 lab project
    @author                     noah tanner, kosimo tonn
    @date                       october, 2023
'''

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

    # imports
    from pyb import Pin, Timer

    # config variables
    ps = 0
    ar = 10
    ch_a_pin = Pin(Pin.cpu.B6, mode=Pin.OUT_PP)
    ch_b_pin = Pin(Pin.cpu.B7, mode=Pin.OUT_PP)
    
    # configure timer for encoder counter
    tim_4 = pyb.Timer(4, period = ar, prescaler = ps)
    tim_4.channel(1, pin=ch_a_pin, mode=pyb.Timer.ENC_AB) #Timer.ENC_AB configures timer in encoder mode, counter changes when ch1 OR ch2 changes
    tim_4.channel(4, pin=ch_b_pin, mode=pyb.Timer.ENC_AB)

    # check the number of elapsed ticks with counter() method of timer obj
    count = tim_4.counter()