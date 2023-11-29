'''
    @name               romi_driver.py
    @brief              new motor driver class that must be used for the romi drivers
    @description        TBD
    @author             tanner, noah
    @date               november, 2023
'''

from pyb import Pin, Timer

class romi_driver:

    def __init__(self, tim, IN1_PWM, IN2_DIR, EN):
        '''
            @name           init
            @brief          initialized 
            @param tim
            @param IN1_PWM
            @param IN2_DIR
            @param EN
        '''
        self.tim    = tim
        self.PWM    = tim.channel(3, pin = IN1_PWM, mode = Timer.PWM)
        self.DIR    = IN2_DIR
        self.EN     = EN

    def set_duty(self, duty: int, dir: int):
        '''
            @name           set_duty
            @brief          method to set duty and direction of motor      
            @param duty     duty cycle between 0 and 100 
            @param dir      0 = forward, 1 = reverse  
        '''
        # set direction
        if dir == 0:
            self.DIR.low()
        elif dir == 1:
            self.dir.high()
        elif (dir != 0) | (dir != 1)
            print('Invalid direction')
        
        # set pwm
        self.pwm.pulse_width_percent(duty)
    
    def enable(self):
        self.EN.high()
    
    def disable(self):
        self.EN.low()
