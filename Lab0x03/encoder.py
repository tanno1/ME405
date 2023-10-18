'''!@file                       main.py
    @brief                      main file for lab0x02 in me405
    @details                    cal poly, san luis obispo me405 lab project
    @author                     noah tanner, kosimo tonn
    @date                       october, 2023
'''
# imports
import motor_class_main as mot_class
from pyb import Pin, Timer
from array import array
import time

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
        self.position       = array( 'L', [0 for n in range(1000)]) 
        self.time           = array( 'L', [0 for n in range(1000)]) 
        self.delta          = array( 'L', [0 for n in range(1000)]) 
        self.idx            = 0
        self.start_time     = 0
        self.end_time       = 0
    
    def start(self, duty_cycle):
        self.duty_cycle     = duty_cycle
        self.motor.enable()
        self.motor.set_duty(self.duty_cycle)
        self.tim.callback(self.tim_cb)
        if self.idx == 999:
            self.tim.callback(None)

    
    def tim_cb(self, tim):
        '''!@brief              timer callback for encoder
            @details
        '''
        # add total position, time, and delta values to respective arrays
        self.encoder.update()                                               # update encoder position
        self.position[self.idx]       = self.encoder.total_position
        self.delta[self.idx]          = self.encoder.current_delta
        self.time[self.idx]           = self.idx
        self.idx += 1
        if self.idx == 999:
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
        self.current_delta = 0          # initialize delta as 0 for first pass
        self.total_position = 0         # initialize total position as 0 for first pass
        self.prev_position = 0          # initialize previous position as 0 for first pass
        self.current_position = 0       # initialize the current position as 0 for first pass

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

if __name__ == "__main__":
    
    ### encoder & motor 1 setup ###

    # encoder 1 configuration 
    ps = 0
    ar = 1000
    ch_a_pin = Pin(Pin.cpu.C7, mode=Pin.OUT_PP)
    ch_b_pin = Pin(Pin.cpu.C6, mode=Pin.OUT_PP)
    tim_8 = Timer(8, period = ar, prescaler = ps)
    cha = tim_8.channel(1, pin=ch_a_pin, mode=Timer.ENC_AB) #Timer.ENC_AB configures timer in encoder mode, counter changes when ch1 OR ch2 changes
    chb = tim_8.channel(2, pin=ch_b_pin, mode=Timer.ENC_AB)

    # motor 1 configuration

    # create a timer object to use for motor control
    mot_tim_A = Timer(3, freq = 20_000)
    # mot_A pin definitions
    mot_EN1 = Pin(Pin.cpu.A10, mode=Pin.OUT_PP)             # motA active high-enable
    mot_IN1 = Pin(Pin.cpu.B4, mode=Pin.OUT_PP)              # motA control pin 1
    mot_IN2 = Pin(Pin.cpu.B5, mode=Pin.OUT_PP)              # motA control pin 2
    mot_A = mot_class.L6206(mot_tim_A, mot_EN1, mot_IN1, mot_IN2)

    # make encoder instance
    encoder_1 = Encoder(tim_8, cha, chb, ar, ps)
    # make collector instance, assign callback method
    tim_6 = Timer(6, freq = 1000)
    collector_1 = collector(tim_6, encoder_1, mot_A)

    ### encoder & motor 2 setup ###

    # encoder 2 configuration
    ch_a_pin_m2 = Pin(Pin.cpu.B6, mode=Pin.OUT_PP)
    ch_b_pin_m2 = Pin(Pin.cpu.B7, mode=Pin.OUT_PP)
    # timer
    tim_4 = Timer(4, period = ar, prescaler = ps)
    cha_mot_2 = tim_4.channel(1, pin=ch_a_pin_m2, mode=Timer.ENC_AB)      # Timer.ENC_AB configures timer in encoder mode, counter changes when ch1 OR ch2 changes
    chb_mot_2 = tim_4.channel(2, pin=ch_b_pin_m2, mode=Timer.ENC_AB)

    # motor 2 configuration

    # create a timer object to use for motor control
    mot_tim_B = Timer(5, freq = 20_000)
    #mot_B pin definitions
    EN2     = Pin(Pin.cpu.C1, mode=Pin.OUT_PP)              # motB active high-enable
    INB_1   = Pin(Pin.cpu.A0, mode=Pin.OUT_PP)              # motB control pin 1
    INB_2   = Pin(Pin.cpu.A1, mode=Pin.OUT_PP)              # motB control pin 2
    mot_B = mot_class.L6206(mot_tim_B, EN2, INB_1, INB_2)

    # make encoder instance
    encoder_2 = Encoder(tim_4, cha_mot_2, chb_mot_2, ar, ps)
    # make collector instance, assign callback method
    tim_7 = Timer(7, freq = 1000)
    collector_2 = collector(tim_7, encoder_2, mot_B)




    

        