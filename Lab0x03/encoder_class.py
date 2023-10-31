'''!@file                       encoder_class.py
    @brief                      encoder/colelctor class, originally from lab0x02
    @details                    cal poly, san luis obispo me405 lab project
    @author                     noah tanner, kosimo tonn
    @date                       october, 2023
'''
# imports
from pyb import Pin, Timer
from array import array
import motor_class as motor
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
        self.long_position  = 0
        self.long_time      = 0
        self.long_delta     = 0
        self.idx            = 0
        self.start_time     = 0
        self.end_time       = 0
        self.type           = 0
        self.old_pos        = 0
    
    def start(self, duty_cycle):
        self.duty_cycle     = duty_cycle
        self.type           = type
        self.encoder.zero()
        self.motor.enable()
        self.motor.set_duty(self.duty_cycle)
        self.tim.callback(self.tim_cb)
        if self.idx == 29999:
            self.tim.callback(None)
    
    def tim_cb(self, tim):
        '''!@brief              timer callback for encoder
            @details
        '''
        self.encoder.update()
        self.long_position             = self.encoder.total_position
        self.long_time                 = self.idx
        self.long_delta                = self.encoder.current_delta
        self.idx += 1
        if self.idx == 29999 and self.type == 2:
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

# encoder mot_a
ps          = 0
ar          = 1000
cha_pin_1   = Pin(Pin.cpu.C7, mode=Pin.OUT_PP)                      # encoder 1, channel a pin
chb_pin_1   = Pin(Pin.cpu.C6, mode=Pin.OUT_PP)                      # encoder 1, channel b pin
tim_a_8     = Timer(8, period = ar, prescaler = ps)                 # encoder 1 timer
cha_1       = tim_a_8.channel(1, pin=cha_pin_1, mode=Timer.ENC_AB)  
chb_1       = tim_a_8.channel(2, pin=chb_pin_1, mode=Timer.ENC_AB)  
enc_1       = Encoder(tim_a_8, cha_1, chb_1, ar, ps)                # encoder 1 instance
# collector mot_a
tim_6       = Timer(6, freq = 1000)                                 # timer for data collection   
collector_1 = collector(tim_6, enc_1, motor.mot_A)                  # collector instance

# encoder mot_b
cha_pin_2   = Pin(Pin.cpu.B6, mode=Pin.OUT_PP)                      # encoder 1, channel a pin
chb_pin_2   = Pin(Pin.cpu.B7, mode=Pin.OUT_PP)                      # encoder 1, channel b pin
tim_a_4     = Timer(4, period = ar, prescaler = ps)                 # encoder 1 timer
cha_2       = tim_a_4.channel(1, pin=cha_pin_2, mode=Timer.ENC_AB)  
chb_2       = tim_a_4.channel(2, pin=chb_pin_2, mode=Timer.ENC_AB)  
enc_2       = Encoder(tim_a_4, cha_2, chb_2, ar, ps)                # encoder 1 instance
# collector mot_b
tim_7       = Timer(7, freq = 1000)                                 # timer for datat collection   
collector_2 = collector(tim_7, enc_2, motor.mot_B)                  # collector instance 
