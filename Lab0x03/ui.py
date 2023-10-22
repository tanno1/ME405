'''
    @file               ui.py
    @brief              class file to control the keyboard input from users and implement results as a generator task function inside of main.py
    @author             noah tanner, kosimo tonn
    @date               october 8th, 2023
'''

# Imports
import ui as ui, encoder_class as encoder, motor_class as motor
import pyb

# variables
valid_commands = ['z', 'Z', 'p', 'P', 'v', 'V', 'm', 'M', 'g', 'G', 'c', 'C', 'k', 'K', 's', 'S', 'r', 'R', 'o', 'O']
# set loop type [ 1 = open, 2 = closed ]
loop_type = 1
done = 0

IS_FLAGS = {
    "DUTY_FLG1" : 0,
    "DUTY_FLG2" : 0,
    "DATA_FLG1" : 0,
    "DATA_FLG2" : 0,
    "CL_FLG1"   : 0,
    "K_FLG1"    : 0,
    "K_FLG2"    : 0,
    "VEL_FLG1"  : 0,
    "VEL_FLG2"  : 0,
    "VALUE"     : 0,
    "VAL_DONE"  : 0
}

# f(n) to choose what command to be executed
def choose_cmnd(command):
    #Zero Encoders
    if command == ('z'):
        encoder.encoder_1.zero()
        print("Encoder 1 zero'd\r\n")
    elif command == ('Z'):
        encoder.encoder_2.zero()
        print("Encoder 2 zero'd\r\n")

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
        state = 'S4_VALUE'
        print('Enter a duty cycle value for motor 1')
    elif command == ('M'):
        # set value enter state
        state = 'S4_VALUE'
        print('Enter a duty cycle value for motor 2')

    # collect speed and position for 30 seconds
    elif command == ('g'):
        pass

    elif command == ('G'):
        pass

    # Switch to Closed-Loop Mode    
    elif command == ('C' or 'c'):
        loop_type = 2
    
    # skip these commands if loop is open
    elif loop_type == 2:  
        # choose closed-loop gains
        if command == ('k'):
            cl_gain_1 = input('Enter a closed loop gain for motor 1: ')
            state = 'S4_VALUE'
        elif command == ('K'):
            cl_gain_2 = input('Enter a closed loop gain for motor 2: ')
            state = 'S4_VALUE'
            
        # choose velocity set point 
        elif command == ('s'):
            vel_set_1 = input('Enter a velocity setpoint for motor 1: ')
            state = 'S4_VALUE'
        elif command == ('S'):
            vel_set_2 = input('Enter a velocity setpoint for motor 2: ')
            state = 'S4_VALUE'
            
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

if __name__ == '__main__':
    #initialization
    pyb.repl_uart(None)                                             # disable uart echoing
    state = 'S0_INIT'                                               # set first state

    while True:
        if state == 'S0_INIT':
            uart = pyb.UART(2, 112500)                              # initialize UART communication 
            vcp = pyb.USB_VCP()                                     # setup vcp object
            state = 'S1_HUB'                                        # set next state

        elif state == 'S1_HUB':
            if vcp.any():                                           # wait for keyboard input
                command = uart.read(1)
                choose_cmnd(command.decode('utf-8'))                    
                state = 'S2_CHRRDY'
        
        elif state == 'S2_CHRRDY':
            charIn_decoded = charIn.decode('utf-8')
            if charIn_decoded in valid_commands:
                state = 'S3_CHOOSE'

        elif state == 'S3_CHOOSE': 
            pass                     

        elif state == 'S4_VALUE':
            # returns a value for a given command (duty cycle, gain), start w/ clearning returned value from previous pass
            returned_value = ''
            ser_idx = 2
            valIn = ser.read(ser_idx).decode()       # read current serial index value
            if valIn.is_digit():
                returned_value.append(valIn)
            elif valIn == '-':
                if ser.idx == 2:
                    returned_value.append(valIn)
            elif valIn == 'X7F':
                if ser.idx != 2:
                    returned_value.pop()
            elif valIn == '\n':
                returned_value = int(returned_value)
                done = 1
            if done == 1:
                state = 'S1_HUB'