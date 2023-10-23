'''
    @file                   cl_gen.py
    @brief                  generator function implementation of the closed loop method
    @author                 noah tanner
    @date                   october 22nd, 2023
'''

# imports
import closed_loop as cl
import encoder_class as encoder
import motor_class as motor
import main

class motor_generator_class:
    '''
        @something                      DoXy Markup stuff
    '''

    def __init__(self, encoder_1, encoder_2, driver_1, driver_2, collector_1, collector_2, flags: dict):
        '''
            @something                  DoXy Markup stuff
        '''
        # motor one variables
        self.encoder_1      = encoder_1
        self.driver_1       = driver_1
        self.collector_1    = collector_1
        self.duty_1         = 0
        self.kp_1           = 0
        self.vel_ref_1      = 0

        # motor two variables
        self.encoder_2      = encoder_2
        self.driver_2       = driver_2
        self.collector_2    = collector_2
        self.duty_2         = 0
        self.kp_2           = 0
        self.vel_ref_2      = 0

        # shared interstate flags for mot 1 & 2
        self.flags          = flags

    def run_gen(self):

        state = 'S0_INIT'

        while True:

            if state == 'S0_INIT':
                DATA_FLGS = {
                    OL_DONE:    False,
                    CL_DONE:    False,
                }
                state = 'S1_HUB'
            
            if state == 'S1_HUB':
                if self.flags['CL_FLG'] == False:
                    state = 'S2_OL'
                elif self.flags['CL_FLG'] == True:
                    state = 'S3_CL'
                else:
                    print("Invalid state, how did we get here?")
            
            if state =='S2_OL':
                if self.flags['DUTY_FLG1'] and self.flags['VAL_DONE']:
                    self.duty_1 = self.flags['VALUE']
                    self.driver_1.set_duty(self.duty_1)
                    self.driver_1.enable()
                if self.flags['DUTY_FLG2'] and self.flags['VAL_DONE']:
                    self.duty_2 = self.flags['VALUE']
                    self.driver_2.set_duty(self.duty_2)
                    self.driver_2.enable()
                if self.flags['DATA_FLG1']:
                    self.collector_1.start(self.duty_1, 2)
                if self.flags['DATA_FLG2']:
                    self.collector_2.start(self.duty_2, 2)

            if state == 'S3_CL':
                closed_loop_mot_a = cl.closed_loop(main.enc_1)
                closed_loop_mot_b = cl.closed_loop(main.enc_2)
                if self.flags['K_FLG1'] and self.flags['VAL_DONE']:
                    closed_loop_mot_a.kp = self.flags['VALUE']
                    new_duty = closed_loop_mot_a.closed_loop()
                elif self.flags['K_FLG2'] and self.flags['VAL_DONE']:
                    closed_loop_mot_b.kp = self.flags['VALUE']
                elif self.flags['VEL_FLG1'] and self.flags['VAL_DONE']:
                    closed_loop_mot_a.vel = self.flags['VALUE']
                elif self.flags['VEL_FLG2'] and self.flags['VAL_DONE']:
                    closed_loop_mot_b.vel = self.flags['VALUE']
                elif self.flags['STEP_FLG1']:
                    pass
                elif self.flags['STEP_FLG2']:
                    pass

            yield(state)