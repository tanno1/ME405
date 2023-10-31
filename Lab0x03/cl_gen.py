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
import export
import time

# set done flags to be initialized
OL_DONE = 0
CL_DONE = 0

class motor_generator_class:
    def __init__(self, encoder_1, encoder_2, driver_1, driver_2, collector_1, collector_2, flags: dict):
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
        closed_loop_mot_a = cl.closed_loop(self.encoder_1)                      # closed loop a instance
        closed_loop_mot_b = cl.closed_loop(self.encoder_2)                      # closed loop b instance

        while True:

            if state == 'S0_INIT':
                #print('Cl: state 0')
                DATA_FLGS = {
                    OL_DONE:    False,
                    CL_DONE:    False,
                }
                state = 'S1_HUB'
            
            if state == 'S1_HUB':
                #print('Cl: state 1')
                if self.flags['CL_FLG'] == False:
                    state = 'S2_OL'
                elif self.flags['CL_FLG'] == True:
                    state = 'S3_CL'
                else:
                    print("Invalid state, how did we get here?")
            
            if state =='S2_OL':
                if self.flags['CL_FLG'] == False:
                    # update encoders at start of each iteration
                    self.encoder_1.update()
                    self.encoder_2.update()
                    # update encoder velocities at start of each iteration
                    self.encoder_1.vel_calc()
                    self.encoder_2.vel_calc()

                    if self.flags['DUTY_FLG1'] and self.flags['VAL_DONE']:
                        self.duty_1 = self.flags['VALUE']
                        self.driver_1.set_duty(self.duty_1)
                        self.driver_1.enable()
                        self.flags['DUTY_FLG1'] = False                         # reset flg
                        self.flags['VAL_DONE'] = False                          # reset flg
                    
                    elif self.flags['DUTY_FLG2'] and self.flags['VAL_DONE']:
                        self.duty_2 = self.flags['VALUE']
                        self.driver_2.set_duty(self.duty_2)
                        self.driver_2.enable()
                        self.flags['DUTY_FLG2'] = False                         # reset flg
                        self.flags['VAL_DONE'] = False                          # reset flg
                    
                    elif self.flags['OLDATA_FLG1']:
                        print('OL data collection started for motor 1')
                        exporter = export.UART_connection()
                        self.driver_1.disable()
                        time.sleep_ms(2000)
                        self.collector_1.start(self.duty_1)
                        while self.collector_1.idx <= 29999:
                            exporter.run(f"{self.collector_1.long_position}\t{self.collector_1.long_time}\t{self.collector_1.long_delta}\r\n")
                        print('OL data colletion finished for motor 1')
                        self.driver_1.disable()
                        self.flags['OLDATA_FLG1'] = False                       # reset flg
                    
                    elif self.flags['OLDATA_FLG2']:
                        print('OL data collection started for motor 2')
                        exporter_2 = export.UART_connection()
                        self.driver_2.disable()
                        time.sleep_ms(2000)
                        self.collector_2.start(self.duty_2)
                        while self.collector_2.idx <= 29999:
                            exporter_2.run(f"{self.collector_2.long_position}\t{self.collector_2.long_time}\t{self.collector_2.long_delta}\r\n")
                        print('OL data colletion finished for motor 2')
                        self.driver_2.disable()
                        self.flags['OLDATA_FLG2'] = False                       # reset flg
                
                elif self.flags['CL_FLG'] == True:
                    state = 'S3_CL'
                else:
                    continue

            if state == 'S3_CL':
                if self.flags['CL_FLG'] == True:
                    if self.flags['K_FLG1'] and self.flags['VAL_DONE']:
                        closed_loop_mot_a.kp = self.flags['VALUE']
                        print('Motor 1 K set to: {}'.format(self.flags['VALUE']))
                        self.flags['K_FLG1'] = False                                        # reset flg        
                        self.flags['VAL_DONE'] = False                                      # reset flg
                    
                    elif self.flags['K_FLG2'] and self.flags['VAL_DONE']:
                        closed_loop_mot_b.kp = self.flags['VALUE']
                        print('Motor 2 K set to: {}'.format(self.flags['VALUE']))
                        self.flags['K_FLG2'] = False                                        # reset flg
                        self.flags['VAL_DONE'] = False                                      # reset flg
                    
                    elif self.flags['VEL_FLG1'] and self.flags['VAL_DONE']:
                        closed_loop_mot_a.vel_ref = self.flags['VALUE']
                        print('Motor 1 V_ref set to: {}'.format(self.flags['VALUE']))
                        self.flags['VEL_FLG1'] = False                                      # reset flg
                        self.flags['VAL_DONE'] = False                                      # reset flg
                    
                    elif self.flags['VEL_FLG2'] and self.flags['VAL_DONE']:
                        closed_loop_mot_b.vel_ref = self.flags['VALUE']
                        print('Motor 2 V_ref set to: {}'.format(self.flags['VALUE']))
                        self.flags['VEL_FLG2'] = False                                      # reset flg
                        self.flags['VAL_DONE'] = False                                      # reset flg

                    elif self.flags['STEP_FLG1']:
                        print('Exporter setup...')
                        exporter = export.UART_connection()
                        print('Driver 1 disabled...')
                        self.driver_1.disable()
                        print('Driver 1 zero\'d')
                        self.encoder_1.zero()
                        time.sleep_ms(2000)
                        print('CL data collection started for motor 1 with Vref: {} and Kp: {}'.format(closed_loop_mot_a.vel_ref, closed_loop_mot_a.kp))
                        self.collector_1.start(self.duty_1)
                        for i in range(30000):
                            self.encoder_1.update()
                            self.encoder_1.vel_calc()
                            exporter.run(f"{self.collector_1.long_position}\t{self.collector_1.long_time}\t{self.collector_1.long_delta}\r\n")
                            new_duty = closed_loop_mot_a.closed_loop()
                            self.driver_1.set_duty(new_duty)
                        self.flags['STEP_FLG1'] = False                 # reset flag
                    elif self.flags['STEP_FLG2']:
                        pass
                elif self.flags['CL_FLG'] == False:
                    state = 'S1_HUB'
                else:
                    continue

            yield(state)