'''
    @name                   imu_driver.py
    @brief                  driver class for the BNO055 IMU sensor from adafruit
    @author                 tanner, noah
    @date                   november, 2023
'''
from pyb import I2C

class bno055:

    def __init__(self, controller: I2C):
        self.controller     = controller
        self.imu_address    = 0x29    
        # registers 
        self.mode_reg           = 'OPR_MODE'
        self.cal_reg            = 'CALIB_STAT'

        self.acc_off_x_l        = 'ACC_OFFSET_X_LSB'
        self.acc_off_x_m        = 'ACC_OFFSET_X_MSB'
        self.acc_off_y_l        = 'ACC_OFFSET_Y_LSB'
        self.acc_off_y_m        = 'ACC_OFFSET_Y_MSB'
        self.acc_off_z_l        = 'ACC_OFFSET_Z_LSB'
        self.acc_off_z_m        = 'ACC_OFFSET_Z_MSB'
        self.acc_offs_list      = [self.acc_off_x_l, self.acc_off_x_m, self.acc_off_y_l, self.acc_off_y_m, self.acc_off_z_l, self.acc_off_z_m]

        self.mag_off_x_l        = 'MAG_OFFSET_X_LSB'
        self.mag_off_x_m        = 'MAG_OFFSET_X_MSB'
        self.mag_off_y_l        = 'MAG_OFFSET_Y_LSB'
        self.mag_off_y_m        = 'MAG_OFFSET_Y_MSB'
        self.mag_off_z_l        = 'MAG_OFFSET_Z_LSB'
        self.mag_off_z_m        = 'MAG_OFFSET_Z_MSB'
        self.mag_offs_list      = [self.mag_off_x_l, self.mag_off_x_m, self.mag_off_y_l, self.mag_off_y_m, self.mag_off_z_l, self.mag_off_z_m]

        self.gyr_off_x_l        = 'GYR_OFFSET_X_LSB'
        self.gyr_off_x_m        = 'GYR_OFFSET_X_MSB'
        self.gyr_off_y_l        = 'GYR_OFFSET_Y_LSB'
        self.gyr_off_y_m        = 'GYR_OFFSET_Y_MSB'
        self.gyr_off_z_l        = 'GYR_OFFSET_Z_LSB'
        self.gyr_off_z_m        = 'GYR_OFFSET_Z_MSB'
        self.gyr_offs_list      = [self.gyr_off_x_l, self.gyr_off_x_m, self.gyr_off_y_l, self.gyr_off_y_m, self.gyr_off_z_l, self.gyr_off_z_m]

        self.acc_rad_l          = 'ACC_RADIUS_LSB'
        self.acc_rad_m          = 'ACC_RADIUS_MSB'
        self.mag_rad_l          = 'MAG_RADIUS_LSB'
        self.mag_rad_m          = 'MAG_RADIUS_MSB'

    def change_mode(self, mode: str):
        self.mode = mode
        '''
            @name           change_mode               
            @brief          method to change the operating mode of the IMU to one of the following fusion modes: X, Y, Z
        '''
        if self.mode == 'IMU':
            reg_value   = 0b1000
            self.controller.mem_write(reg_value, self.imu_adress, self.mode_reg , timeout = 1000 )
            print('Mode changes to IMU')
        elif self.mode == 'COMPASS':
            reg_value   = 0b1001
            self.controller.mem_write(reg_value, self.imu_adress, self.mode_reg , timeout = 1000 )
            print('Mode changes to COMPASS')
        elif self.mode == 'M4G':
            reg_value   = 0b1010
            self.controller.mem_write(reg_value, self.imu_adress, self.mode_reg , timeout = 1000 )
            print('Mode changes to M4G')
        elif self.mode == 'NDOF_FMC_OFF':
            reg_value   = 0b1011
            self.controller.mem_write(reg_value, self.imu_adress, self.mode_reg , timeout = 1000 )
            print('Mode changes to NDOF_FMC_OFF')
        elif self.mode == 'NDOF':
            reg_value   = 0b1100
            self.controller.mem_write(reg_value, self.imu_adress, self.mode_reg , timeout = 1000 )
            print('Mode changes to NDOF')
        else:
            print('Invalid mode')

    def cal_status(self):

        '''
            @name           calibration_status
            @brief          retrieves calibration status from the imu and parse into individual statuses           
        '''
        cal_status  = self.controller.mem_read(8, self.imu_address, self.cal_reg)                                                           # read cal_status, return a bytes object                                               
        first_parse = [int.from_bytes(cal_status[i:i+2], byteorder='big', signed=False) for i in range(0, len(cal_status), 2)]              # parse and convert bytes to bin ints
        cal_ints    = [int(''.join(map(str, first_parse[i:i+2])), 2) for i in range(0, len(first_parse), 2)]                                # parse and convert bin ints to int

        # print calibration statuses to terminal
        # print(f'SYS Calib Status: {"Calibrated" if cal_ints[0] == 3, else "Not Calibrated"}')
        # print(f'GYR Calib Status: {"Calibrated" if cal_ints[1] == 3, else "Not Calibrated"}')
        # print(f'ACC Calib Status: {"Calibrated" if cal_ints[2] == 3, else "Not Calibrated"}')
        # print(f'MAG Calib Status: {"Calibrated" if cal_ints[3] == 3, else "Not Calibrated"}')    

    def get_cal_coeff(self):
        acc_off = [ 0, 0, 0, 0, 0, 0 ]
        mag_off = [ 0, 0, 0, 0, 0, 0 ]
        gyr_off = [ 0, 0, 0, 0, 0, 0 ]
        '''
            @name           get_cal_coeff
            @brief          retrieves calibration coefficients from IMU as an array of packed binary data once cal status checks out
        '''
        for i in self.acc_offs_list:
            for j in acc_off:
                acc_off[j] = self.controller.mem_read(1, self.imu_address, self.acc_offs_list[i])

        for i in self.mag_offs_list:
            for j in mag_off:
                gyr_off[j] = self.controller.mem_read(1, self.imu_address, self.mag_offs_list[i])

        for i in self.gyr_offs_list:
            for j in gyr_off:
                gyr_off[j] = self.controller.mem_read(1, self.imu_address, self.gyr_offs_list[i])

    def write_cal_coeff(self, acc_bytes, mag_bytes, gyr_bytes)
    '''
        @name               write_cal_coeff
        @brief              method to write calibration coefficients back to the IMU from pre-recorded packed binary data
    '''
        for bit in acc_bytes:
            for reg in self.acc_offs_list:
                self.controller.mem_write(bit, self.imu_address, reg, timeout = 1000)

        for bit in mag_bytes:
            for reg in self.mag_offs_list:
                self.controller.mem_write(bit, self.imu_address, reg, timeout = 1000)

        for bit in mag_bytes:
            for reg in self.mag_offs_list:
                self.controller.mem_write(bit, self.imu_address, reg, timeout = 1000)
                
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

# create controller
controller = I2C(1, I2C.controller)

# create bno055 objects
imu = bno055(controller)