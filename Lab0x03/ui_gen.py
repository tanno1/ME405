'''
    @file            ui_gen.py
    @brief           generator function file built from standalone ui file
    @author          noah tanner
    @date            october 22nd, 2023
'''

# imports
import encoder_class as encoder
import motor_class as motor
import pyb

valid_commands = ['z', 'Z', 'p', 'P', 'v', 'V', 'm', 'M', 'g', 'G', 'c', 'C', 'k', 'K', 's', 'S', 'r', 'R', 'o', 'O']
done = False

# flags setup
IS_FLAGS = {
        "DUTY_FLG1"     : False,                    # ol  
        "DUTY_FLG2"     : False,                    #
        "OLDATA_FLG1"   : False,                    #
        "OLDATA_FLG2"   : False,                    #
        "CL_FLG"        : False,                    # switch ol / cl
        "STEP_FLG1"     : False,                    # cl
        "STEP_FLG2"     : False,                    #
        "K_FLG1"        : False,                    #
        "K_FLG2"        : False,                    #
        "VEL_FLG1"      : False,                    #
        "VEL_FLG2"      : False,                    #
        "VAL_DONE"      : False,                    #
        "VALUE"         : 0,                        #
    }

# f(n) to choose what command to be executed
def choose_cmnd(command):
    #Zero Encoders
    if command == ('z'):
        print("Encoder 1 zero'd")
        encoder.enc_1.zero()
    elif command == ('Z'):
        print("Encoder 2 zero'd")
        encoder.enc_2.zero()

    # print position
    elif command == ('p'):
        pos = encoder.enc_1.get_position()
        print("Position of encoder 1: {}".format(pos))
    elif command == ('P'):
        pos = encoder.enc_2.get_position()
        print("Position of encoder 2: {}".format(pos))
    
    # print delta
    elif command == ('d'):
        delta = encoder.enc_1.get_delta()
        print("Delta of en encoder 1: {}".format(delta))
    elif command == ('D'):
        delta = encoder.enc_2.get_delta()
        print("Delta of en encoder 2: {}".format(delta))

    # print Velocity     
    elif command == ('v'):
        print('Velocity of encoder 1: {} rad/s or {} rpm'.format(encoder.enc_1.velocity['rad/s'], encoder.enc_1.velocity['rpm']))
    elif command == ('V'):
        print('Velocity of encoder 2: {} rad/s or {} rpm'.format(encoder.enc_2.velocity['rad/s'], encoder.enc_2.velocity['rpm']))

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
        IS_FLAGS['OLDATA_FLG1'] = True
    elif command == ('G'):
        IS_FLAGS['OLDATA_FLG2'] = True

    # Switch to Closed-Loop Mode    
    elif command == ('c'):
        IS_FLAGS['CL_FLG'] = True
    elif command == ('C'):
        IS_FLAGS['CL_FLG'] = True
            
    # skip these commands if loop is open
    elif IS_FLAGS['CL_FLG'] == True:  
        print('UI: in CL section')
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
            IS_FLAGS['CL_FLG'] = False
        elif command == 'O':
            IS_FLAGS['CL_FLG'] = False


def ui_gen():
    takes_input = ['DUTY_FLG1', 'DUTY_FLG2', 'K_FLG1', 'K_FLG2', 'VEL_FLG1', 'VEL_FLG2']
    state = 'S0_INIT'
    returned_value = ''
    
    while True:

        if state == 'S0_INIT':
            vcp = pyb.USB_VCP()
            print("Awaiting the next command...")
            state = 'S1_HUB'

        elif state == 'S1_HUB':
            #print("UI: in state 1")
            if vcp.any():                                           
                command = vcp.read(1)
                choose_cmnd(command.decode('utf-8'))
                if any(IS_FLAGS[key] == 1 for key in takes_input):
                    state = 'S2_CHRRDY'
            
        elif state == 'S2_CHRRDY':  
            print("UI: in state 2")
            done = False
            returned_value = ''                                     # reset the returned value string
            while not done:
                if vcp.any():
                    valIn = vcp.read(1).decode()                    # read current serial index value
                    print(valIn, end='')
                    idx = 1                                         # set str index to 1
                    if valIn.isdigit():                             # check if digit
                        returned_value += valIn                     
                        idx += 1
                    elif valIn == '.':
                        if idx == 1:
                            returned_value += valIn
                    elif valIn == '-':                              # check if minus
                        if idx == 1:                                 
                            returned_value += valIn                 
                    elif valIn == 'X7F':                            # check if backspace
                        if idx != 2:                                
                            returned_value = returned_value[:-1]            
                    elif valIn == '\n' or valIn == '\r':            # check if enter or carridge return 
                        try:
                            returned_value = int(returned_value)
                        except ValueError:
                            returned_value = float(returned_value)        
                        done = True                                 # complete the state

            state = 'S1_HUB'                                        # set next state back to hub
            IS_FLAGS['VAL_DONE'] = True                             # set value done flag, picked up by main
            IS_FLAGS['VALUE'] = returned_value                      # set value
            print("value: {}".format(IS_FLAGS['VALUE']))
            done = False                                            # reset done flag
        
        yield(state)