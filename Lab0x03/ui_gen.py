'''!@file            ui_gen.py
    @brief           generator function file built from standalone ui file
'''

# imports
import encoder_class as encoder, motor_class as motor
import pyb

S0_INIT     = 0
S1_HUB      = 1
S2_CHRRDY   = 2

state = 0
valid_commands = ['z', 'Z', 'p', 'P', 'v', 'V', 'm', 'M', 'g', 'G', 'c', 'C', 'k', 'K', 's', 'S', 'r', 'R', 'o', 'O']
loop_type = 1
done = 0

# f(n) to choose what command to be executed
def choose_cmnd(command):
    # allow usage of loop type
    global loop_type

    #Zero Encoders
    if command == ('z'):
        print("Encoder 1 zero'd\r\n")
        encoder.encoder_1.zero()
    elif command == ('Z'):
        print("Encoder 2 zero'd\r\n")
        encoder.encoder_2.zero()

    # print position
    elif command == ('p'):
        pos = encoder.encoder_1.get_position()
        print("Position of en encoder 1: {}\r\n".format(pos))
    elif command == ('p'):
        pos = encoder.encoder_2.get_position()
        print("Position of en encoder 2: {}\r\n".format(pos))
    
    # print position
    elif command == ('p'):
        pos = encoder.encoder_1.get_position()
        print("Position of en encoder 1: {}\r\n".format(pos))
    elif command == ('p'):
        pos = encoder.encoder_2.get_position()
        print("Position of en encoder 2: {}\r\n".format(pos))

    # print Velocity     
    elif command == ('v'):
        print('Velocity of encoder 1: {} rad/s or {} rpm'.format(encoder.encoder_1.velocity['rad/s'], encoder.encoder_1.velocity['rpm']))
    elif command == ('V'):
        print('Velocity of encoder 2: {} rad/s or {} rpm'.format(encoder.encoder_2.velocity['rad/s'], encoder.encoder_2.velocity['rpm']))

    # enter a duty cycle   
    elif command == ('m'):
        # set value enter state
        print('Enter a duty cycle value for motor 1')
        IS_FLAGS['DUTY_FLG1'] = True
    elif command == ('M'):
        # set value enter state
        print('Enter a duty cycle value for motor 2')
        IS_FLAGS['DUTY_FLG2'] = True

    # collect speed and position for 30 seconds
    elif command == ('g'):
        pass

    elif command == ('G'):
        pass

    # Switch to Closed-Loop Mode    
    elif command == ('c'):
        loop_type = 2
    
    # skip these commands if loop is open
    elif loop_type == 2:  
        # choose closed-loop gains
        if command == ('k'):
            print('Enter a closed-loop gain value for motor 1')
            IS_FLAGS['K_FLG1'] = True
        elif command == ('K'):
            print('Enter a closed-loop gain value for motor 2')
            IS_FLAGS['K_FLG2'] = True
            
        # choose velocity set point 
        elif command == ('s'):
            print('Enter a velocity value for motor 1')
            IS_FLAGS['VEL_FLG1'] = True
        elif command == ('S'):
            print('Enter a velocity value for motor 2')
            IS_FLAGS['VEL_FLG2'] = True
            
        # trigger step response and send data to be plott'd
        elif command == ('r'):
            # step response f(n) mot 1
            pass
        elif command == ('R'):
            # step response f(n) mot 2
            pass

        # set open loop again
        elif command == 'o':
            loop_type = 1
        elif command == 'O':
            loop_type = 1


def ui_gen():
    # initial variable configuration
    IS_FLAGS = {
        "DUTY_FLG1" : False,
        "DUTY_FLG2" : False,
        "DATA_FLG1" : False,
        "DATA_FLG2" : False,
        "CL_FLG1"   : False,
        "CL_FLG2"   : False,
        "K_FLG1"    : False,
        "K_FLG2"    : False,
        "VEL_FLG1"  : False,
        "VEL_FLG2"  : False,
        "VALUE"     : 0,
        "VAL_DONE"  : False
    }
    takes_input = ['DUTY_FLG1', 'DUTY_FLG2', 'K_FLG1', 'K_FLG2', 'VEL_FLG1', 'VEL_FLG2']
    state = 0

    while(True):

        if state == S0_INIT:
            uart = pyb.UART(2, 112500)
            vcp = pyb.USB_VCP()
            print("Awaiting the next command...")
            state = 'S1_HUB'

        elif state == S1_HUB:
            if vcp.any():                                           
                command = vcp.read(1)
                choose_cmnd(command.decode('utf-8'))
                if any(IS_FLAGS[key] == 1 for key in takes_input):
                    state = 'S2_CHRRDY'
            
        elif state == S2_CHRRDY:    
            passreturned_value = ''                                     # reset the returned value string
            while not done:
                if vcp.any():
                    valIn = vcp.read(1).decode()                    # read current serial index value
                    print(valIn, end='')
                    idx = 1                                         # set str index to 1
                    if valIn.isdigit():                             # check if digit
                        returned_value += valIn                     #
                        idx += 1
                    elif valIn == '-':                              # check if minus
                        if idx == 2:                                # 
                            returned_value += valIn                 #
                    elif valIn == 'X7F':                            # check if backspace
                        if idx != 2:                                #
                            returned_value = returned_value[:-1]    #        
                    elif valIn == '\n' or valIn == '\r':            # check if enter or carridge return  
                        returned_value = int(returned_value)        #
                        done = True                                 # complete the state

            state = 'S1_HUB'                                        # set next state back to hub
            IS_FLAGS['VAL_DONE'] = True                             # set value done flag, picked up by main
            done = False                                            # reset done flag