'''
    @name                   imu_driver.py
    @brief                  driver class for the BNO055 IMU sensor from adafruit
    @author                 tanner, noah
    @date                   november, 2023
'''

class bno55:

    def __init__(self):
        pass

    def change_mode(self):
        '''
            @name           change_mode               
            @brief          method to change the operating mode of the IMU to one of the following fusion modes: X, Y, Z
        '''
        pass

    def cal_status(self):
        '''
            @name           calibration_status
            @brief          retrieves calibration status from the imu and parse into individual statuses           
        '''
        pass

    def cal_coeff(self):
        '''
            @name           cal_status
            @brief          retrieves calibration coefficients from IMU as an array of packed binary data
        '''
    
    def euler(self):
        '''
            @name           euler
            @brief          reads euler angles from IMU to use as measurements for feedback
        '''
    
    def ang_vel(self):
        '''
            @name           angular velocity
            @brief          reads angular velocity from the IMU to use as measurements for feedback    
        '''