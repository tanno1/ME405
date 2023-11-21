'''
    @name                   imu_driver.py
    @brief                  driver class for the BNO055 IMU sensor from adafruit
    @author                 tanner, noah
    @date                   november, 2023
'''
from pyb import I2C

def combine_bytes(msb, lsb):
    combined_value = ( msb << 8 ) | lsb
    return combined_value

def combine_to_decimal(combined_bytes):
    if combined_bytes & 0x8000:
        combined_values = combined_bytes - 0x10000
    
    return combined_values

class bno055:

    def __init__(self, controller: I2C):
        self.controller         = controller
        self.imu_address        = 0x28
        # registers 
        self.mode_reg           = 0x3D
        self.cal_reg            = 0x35

        self.acc_off_x_l        = 0x55
        self.acc_off_x_m        = 0x56
        self.acc_off_y_l        = 0x57
        self.acc_off_y_m        = 0x58
        self.acc_off_z_l        = 0x59
        self.acc_off_z_m        = 0x5A
        self.acc_offs_list      = [ self.acc_off_x_l, 
                                    self.acc_off_x_m, 
                                    self.acc_off_y_l, 
                                    self.acc_off_y_m, 
                                    self.acc_off_z_l, 
                                    self.acc_off_z_m ]

        self.mag_off_x_l        = 0x5B
        self.mag_off_x_m        = 0x56C
        self.mag_off_y_l        = 0x5D
        self.mag_off_y_m        = 0x5E
        self.mag_off_z_l        = 0x5F
        self.mag_off_z_m        = 0x60
        self.mag_offs_list      = [ self.mag_off_x_l, 
                                    self.mag_off_x_m, 
                                    self.mag_off_y_l, 
                                    self.mag_off_y_m, 
                                    self.mag_off_z_l, 
                                    self.mag_off_z_m ]

        self.gyr_off_x_l        = 0x61
        self.gyr_off_x_m        = 0x62
        self.gyr_off_y_l        = 0x63
        self.gyr_off_y_m        = 0x64
        self.gyr_off_z_l        = 0x65
        self.gyr_off_z_m        = 0x66
        self.gyr_offs_list      = [ self.gyr_off_x_l, 
                                    self.gyr_off_x_m, 
                                    self.gyr_off_y_l, 
                                    self.gyr_off_y_m, 
                                    self.gyr_off_z_l, 
                                    self.gyr_off_z_m]

        self.acc_rad_l          = 0x67
        self.acc_rad_m          = 0x68
        self.mag_rad_l          = 0x69
        self.mag_rad_m          = 0x6A

        self.eul_pitch_l        = 0x1A
        self.eul_pitch_m        = 0x1B
        self.eul_roll_l         = 0x1C
        self.eul_roll_m         = 0x1D
        self.eul_head_l         = 0x1E
        self.eul_head_m         = 0x1F
        self.euler_meas_list    = [ self.eul_pitch_m, 
                                    self.eul_pitch_l, 
                                    self.eul_roll_m, 
                                    self.eul_roll_l, 
                                    self.eul_head_m, 
                                    self.eul_head_l ]

        self.gyr_x_l            = 0x14
        self.gyr_x_m            = 0x15
        self.gyr_y_l            = 0x16
        self.gyr_y_m            = 0x17
        self.gyr_z_l            = 0x18
        self.gyr_z_m            = 0x19
        self.gyr_list           = [ self.gyr_x_m,
                                    self.gyr_x_l,
                                    self.gyr_y_m,
                                    self.gyr_y_l,
                                    self.gyr_z_m,
                                    self.gyr_z_l ]

    def change_mode(self, mode: str):
        self.mode = mode
        '''
            @name           change_mode               
            @brief          method to change the operating mode of the IMU to one of the following fusion modes: X, Y, Z
        '''
        if self.mode == 'IMU':
            reg_value   = 0b1000
            self.controller.mem_write(reg_value, self.imu_address, self.mode_reg , timeout = 1000)
            print('Mode changed to IMU')
        elif self.mode == 'COMPASS':
            reg_value   = 0b1001
            self.controller.mem_write(reg_value, self.imu_address, self.mode_reg , timeout = 1000 )
            print('Mode changeD to COMPASS')
        elif self.mode == 'M4G':
            reg_value   = 0b1010
            self.controller.mem_write(reg_value, self.imu_address, self.mode_reg , timeout = 1000 )
            print('Mode changed to M4G')
        elif self.mode == 'NDOF_FMC_OFF':
            reg_value   = 0b1011
            self.controller.mem_write(reg_value, self.imu_address, self.mode_reg , timeout = 1000 )
            print('Mode changed to NDOF_FMC_OFF')
        elif self.mode == 'NDOF':
            reg_value   = 0b1100
            self.controller.mem_write(reg_value, self.imu_address, self.mode_reg , timeout = 1000 )
            print('Mode changed to NDOF')
        else:
            print('Invalid mode')

    def cal_status(self):

        '''
            @name           calibration_status
            @brief          retrieves calibration status from the imu and parse into individual statuses           
        '''
        cal_status  = self.controller.mem_read(8, self.imu_address, self.cal_reg, addr_size=8)                                                           # read cal_status, return a bytes object                                               
        first_parse = [int.from_bytes(cal_status[i:i+2], byteorder='big', signed=False) for i in range(0, len(cal_status), 2)]              # parse and convert bytes to bin ints
        cal_ints    = [int(''.join(map(str, first_parse[i:i+2])), 2) for i in range(0, len(first_parse), 2)]                                # parse and convert bin ints to int
        print(cal_ints)
        return cal_ints

    def get_cal_coeff(self):
        '''
            @name           get_cal_coeff
            @brief          retrieves calibration coefficients from IMU as an array of packed binary data once cal status checks out
        '''
        acc_off = [ 0, 0, 0, 0, 0, 0 ]
        mag_off = [ 0, 0, 0, 0, 0, 0 ]
        gyr_off = [ 0, 0, 0, 0, 0, 0 ]

        for i in self.acc_offs_list:
            for j in acc_off:
                acc_off[j] = self.controller.mem_read(1, self.imu_address, self.acc_offs_list[i])

        for i in self.mag_offs_list:
            for j in mag_off:
                gyr_off[j] = self.controller.mem_read(1, self.imu_address, self.mag_offs_list[i])

        for i in self.gyr_offs_list:
            for j in gyr_off:
                gyr_off[j] = self.controller.mem_read(1, self.imu_address, self.gyr_offs_list[i])

    def write_cal_coeff(self, acc_bytes: bytes, mag_bytes: bytes, gyr_bytes: bytes):
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
        eul_meas_bytes = [ 0, 0, 0, 0, 0, 0 ]

        for reg in self.euler_meas_list:
            for idx in range(6):
                byte = self.controller.mem_read(8, self.imu_address, reg)
                eul_meas_bytes[idx] = byte
                idx += 1
        # slice list into individual msb, lsb for each euler measurement
        eul_pitch   = eul_meas_bytes[:2]
        eul_head    = eul_meas_bytes[2:4]
        eul_roll    = eul_meas_bytes[4:]

        # combine msb, lsb bytes
        eul_pitch   = combine_bytes(eul_pitch[0], eul_pitch[1])
        eul_head    = combine_bytes(eul_head[0], eul_head[1])
        eul_roll    = combine_bytes(eul_roll[0], eul_roll[1])

        # convert bytes to decimals
        eul_pitch   = combine_to_decimal(eul_pitch)
        eul_head    = combine_to_decimal(eul_head)
        eul_roll    = combine_to_decimal(eul_roll)

        return eul_pitch, eul_head, eul_roll

    def ang_vel(self):
        '''
            @name           angular velocity
            @brief          reads angular velocity from the IMU to use as measurements for feedback    
        '''
        gyr_meas_bytes = [ 0, 0, 0, 0, 0, 0 ]

        for reg in self.gyr_list:
            for idx in range(6):
                byte = self.controller.mem_read(8, self.imu_address, reg)
                gyr_meas_bytes[idx] = byte
                idx += 1
        # slice list into individual msb, lsb for each axis
        gyr_x   = gyr_meas_bytes[:2]
        gyr_y   = gyr_meas_bytes[2:4]
        gyr_z   = gyr_meas_bytes[4:]
        
        #combine msb, lsb
        gyr_x   = combine_bytes(gyr_x[0], gyr_x[1])
        gyr_y   = combine_bytes(gyr_y[0], gyr_y[1])
        gyr_z   = combine_bytes(gyr_z[0], gyr_z[1])

        # converts bytes to decimal
        gyr_x   = combine_to_decimal(gyr_x)
        gyr_y   = combine_to_decimal(gyr_y)
        gyr_z   = combine_to_decimal(gyr_z)

        return gyr_x, gyr_y, gyr_z

if __name__ == '__main__':
    # create controller
    i2c = I2C(1, I2C.CONTROLLER)
    i2c.init(I2C.CONTROLLER, baudrate=400_000)

    # create bno055 objects
    imu = bno055(i2c)