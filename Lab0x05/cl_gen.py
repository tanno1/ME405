'''
    @file                   cl_gen.py
    @brief                  generator function implementation of the closed loop method
    @author                 noah tanner
    @date                   october 22nd, 2023
'''

# imports
import controls

class motor_generator_class:
    def __init__(self, encoder_1, encoder_2, driver_1, driver_2, imu, flags: dict):
        # motor one variables
        self.encoder_1      = encoder_1
        self.driver_1       = driver_1

        # motor two variables
        self.encoder_2      = encoder_2
        self.driver_2       = driver_2

        # other
        self.imu            = imu
        self.flags          = flags

    def run_gen(self):
        state = 'S1_HUB'
       # closed loop b instance

        while True:
            
            if state == 'S1_HUB':

                if self.flags['NORTH'] == True:
                    while not north:
                        current_euler = self.imu.euler()
                        controls.left(0, 25)
                        if current_euler[2] == 0:
                            controls.stop()
                            north = True
                    print('facing north')
                    self.flags['NORTH'] = False
        
            yield(state)