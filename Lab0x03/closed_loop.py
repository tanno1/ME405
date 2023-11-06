'''!@file                       closed_loop.py
    @brief                      closed loop P, PI, PID implementation
    @details                    cal poly, san luis obispo me405 lab project
    @author                     noah tanner, kosimo tonn
    @date                       october, 2023
'''

# imports
import encoder_class as encoder
import motor_class as motor
import time

class closed_loop:
    '''!@brief                  closed loop controls implementation class
        @details                this class allows for P, PI, or PID controls calculations and implementation for the dc motor.
    '''

    def __init__(self, encoder: encoder.Encoder, motor: motor.L6206):
        '''!@brief              creates a closed loop object
            @param  encoder:    an encoder object for feedback from dc motor
            @type   encoder:    encoder_class
            @param  vel_ref:    a reference velocity used in calculation of error [rad/s]
            @type   vel_ref:    integer 

            @return:            signed duty cycle, L, to be applied to the motor
            @rtype:             integer  
        '''
        self.encoder    = encoder
        self.motor      = motor
        self.vel_ref    = 0
        self.vel_meas   = 0
        self.vel_err    = 0
        self.kp         = 0
        self.l          = 0

    def closed_loop(self):
        self.vel_meas   = int(self.encoder.velocity['rpm'])
        self.vel_err    = int(self.vel_ref - self.vel_meas)
        self.l          = int(self.vel_err * self.kp)
        if self.l > 100: 
            self.l = 100                                    
        if self.l < 0:                                    
            self.l = 0
        
        # print(f'new duty: {self.l}')
        
        return self.l
        
        

        
