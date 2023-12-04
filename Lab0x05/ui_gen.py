'''
    @file            ui_gen.py
    @brief           generator function file built from standalone ui file
    @author          noah tanner
    @date            october 22nd, 2023
'''

# imports
import pyb
import imu_driver as imu

valid_commands  = ['e', 'v', 'vn']
done            = False

# flags setup
IS_FLAGS = {
        "NORTH"         : False,                    # face north
        "VALUE"         : 0,
    }

# f(n) to choose what command to be executed
def choose_cmnd(command):
    if command not in valid_commands:
        print('Invalid command')
    # print euler angles
    if command == ('e'):
        imu.imu_obj.euler()
    elif command == ('v'):
        imu.imu_obj.ang_vel()
    elif command == ('n'):
        imu.face_north(imu.imu_obj)

def ui_gen():
    state = 'S0_INIT'
    print('there')
    
    while True:
        if state == 'S0_INIT':
            vcp = pyb.USB_VCP()
            print("Awaiting the next command...")
            state = 'S1_HUB'

        elif state == 'S1_HUB':
            if vcp.any():                                           
                command = vcp.read(1)
                choose_cmnd(command.decode('utf-8'))
        
        yield(state)