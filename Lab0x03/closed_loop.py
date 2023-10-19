'''!@file                       closed_loop.py
    @brief                      closed loop P, PI, PID implementation
    @details                    cal poly, san luis obispo me405 lab project
    @author                     noah tanner, kosimo tonn
    @date                       october, 2023
'''

# imports
import encoder_class as encoder, motor_class as encoder

class closed_loop:
    '''!@brief                  closed loop controls implementation class
        @details                this class allows for P, PI, or PID controls calculations and implementation for the dc motor.
    '''

    def __init__(self, encoder, vel_ref):
        '''!@brief              creates a closed loop object
            @param  encoder:    an encoder object for feedback from dc motor
            @type   encoder:    encoder_class
            @param  vel_ref:    a reference velocity used in calculation of error [rad/s]
            @type   vel_ref:    integer 

            @return:            signed duty cycle, L, to be applied to the motor
            @rtype:             integer  
        '''
        self.encoder    = encoder
        self.vel_ref    = vel_ref
        self.kp         = 100       # need actual value for kp determined from open loop test I believe?
        self.l          = 0

    def closed_loop(self):
        self.l = vel_ref - 
