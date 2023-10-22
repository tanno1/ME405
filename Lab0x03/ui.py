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

def uart_print():
    if uart.any():
        uart_mess = uart.read()
        print(uart_mess.decode('utf-8'))

if __name__ == '__main__':
    pyb.repl_uart(None)
    state = 'S0_INIT'

    if state == 'S0_INIT':
        # initialize UART communication
        uart = pyb.UART(2, 112500)
        # initialize vcp object
        ser = pyb.USB_VCP()
        # print with uart over term 1
        state = 'S1_HUB'

    if state == 'S1_HUB':
        if uart.any():
            charIn = uart.read(1)
            state = 'S2_CHRRDY'
    
    if state == 'S2_CHRRDY':
        charIn_decoded = charIn.decode('utf-8')
        if charIn_decoded in valid_commands:
            state = 'S3_CHOOSE'

    if state == 'S3_CHOOSE':
        #Zero Encoders
        if charIn_decoded == ('z'):
            encoder.encoder_1.zero()
            mess = uart.write("Encoder 1 zero'd\r\n")
            uart_print()
        elif charIn_decoded == ('Z'):
            encoder.encoder_2.zero()
            mess = uart.write("Encoder 2 zero'd\r\n")
            uart_print()

        # print position
        elif charIn_decoded == ('p'):
            pos = encoder.encoder_1.get_position()
            mess = uart.write("Position of en encoder 1: {}\r\n".format(pos))
            uart.print()
        elif charIn_decoded == ('p'):
            pos = encoder.encoder_2.get_position()
            mess = uart.write("Position of en encoder 2: {}\r\n".format(pos))
            uart_print()
            
        # print Velocity     
        elif charIn_decoded == ('v'):
            mess = uart.write('Velocity of encoder 1: {} rad/s or {} rpm'.format(encoder.encoder_1.velocity['rad/s'], encoder.encoder_1.velocity['rpm']))
            uart_print()
        elif charIn_decoded == ('V'):
            mess = uart.write('Velocity of encoder 2: {} rad/s or {} rpm'.format(encoder.encoder_2.velocity['rad/s'], encoder.encoder_2.velocity['rpm']))
            uart_print()
        
        # enter a duty cycle   
        elif charIn_decoded == ('m'):
            # set value enter state
            state = 'S4_VALUE'
            mess = uart.write('Enter a duty cycle value for motor 1')
            uart_print()
        elif charIn_decoded == ('M'):
            # set value enter state
            state = 'S4_VALUE'
            mess = uart.write('Enter a duty cycle value for motor 2')
            uart_print()
            
        # collect speed and position for 30 seconds
        if charIn_decoded == ('g'):
            pass

        if charIn_decoded == ('G'):
            pass
  
        # Switch to Closed-Loop Mode    
        if charIn_decoded == ('C' or 'c'):
            loop_type = 2
        
        # skip these commands if loop is open
        if loop_type == 2:  
            # choose closed-loop gains
            if charIn_decoded == ('k'):
                cl_gain_1 = input('Enter a closed loop gain for motor 1: ')
                state = 'S4_VALUE'
            if charIn_decoded == ('K'):
                cl_gain_2 = input('Enter a closed loop gain for motor 2: ')
                state = 'S4_VALUE'
                
            # choose velocity set point 
            if charIn_decoded == ('s'):
                vel_set_1 = input('Enter a velocity setpoint for motor 1: ')
                state = 'S4_VALUE'
            if charIn_decoded == ('S'):
                vel_set_2 = input('Enter a velocity setpoint for motor 2: ')
                state = 'S4_VALUE'
                
            # trigger step response and send data to be plott'd
            if charIn_decoded == ('r'):
                # step response f(n) mot 1
                pass
            if charIn_decoded == ('R'):
                # step response f(n) mot 2
                pass

            # set open loop again
            if charIn_decoded == 'o':
                loop_type = 1
            if charIn_decoded == 'O':
                loop_type = 1
        
        if state == 'S4_VALUE':
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
            













# #Main
# while True:
    # # wait for valid command to be entered
    # while len(key) != 1 or key not in valid_commands
    #     key = input('Enter a command: ')
    #     print('Invalid command, try again.')

    # #Zero Encoders
    # elif key == ('z'):
    #     encoder.encoder_1.zero()
    #     print('Position of encoder 1 zero\'d') 
    # elif key == ('Z'):
    #     encoder.encoder_2.zero()
    #     print('Position of encoder 2 zero\'d')

    # # print position
    # elif key == ('p'):
    #     print('Position of encoder 1: {}'.format(encoder.encoder_1.current_position))
    # elif key == ('p'):
    #     print('Position of encoder 2: {}'.format(encoder.encoder_2.current_position)) 

    # # print Velocity     
    # if key == ('v'):
    #     print('Velocity of encoder 1: {} rad/s or {} rpm'.format(encoder.encoder_1.velocity['rad/s'], encoder.encoder_1.velocity['rpm']))
    # if key == ('V'):
    #     print('Velocity of encoder 2: {} rad/s or {} rpm'.format(encoder.encoder_2.velocity['rad/s'], encoder.encoder_2.velocity['rpm']))
      
    # # enter a duty cycle   
    # if key == ('m'):
    #     while duty_cycle_1 not in range(-100, 101) or duty_cycle_1 not float:
    #         duty_cycle_1 = input('Enter a duty cycle for motor 1: ')
    #         print('Enter a valid integer from -100 to 100')
    #     motor.mot_A.set_duty(duty_cycle_1)
    #     print('Duty cycle for motor 1 set to {}'.format(duty_cycle_1))

    # if key == ('M'):
    #     while duty_cycle_2 not in range(-100, 101) or duty_cycle_2 not float:
    #         duty_cycle_2 = input('Enter a duty cycle for motor 2: ')
    #         print('Enter a valid integer from -100 to 100')
    #     motor.mot_B.set_duty(duty_cycle_2)
    #     print('Duty cycle for motor 2 set to {}'.format(duty_cycle_2))
        
    # # collect speed and position for 30 seconds
    # if key == ('g'):
    #     encoder.encoder_1.start(duty_cycle_1, 2)
    #     print('Collecting encoder 1 speed and position')
    #     while encoder.encoder_1.idx != 29999:
    #         time.sleep(1)
    #         print('Collecting data...')

    # if key == ('G'):
    #     encoder.encoder_2.start(duty_cycle_2, 2)
    #     print('Collecting encoder 2 speed and position')
    #     while encoder.encoder_2.idx != 29999:
    #         time.sleep(1)
    #         print('Collecting data...')

        
    # # Switch to Closed-Loop Mode    
    # if key == ('C' or 'c'):
    #     loop_type = 2
    
    # # skip these commands if loop is open
    # if loop_type = 2:  
    #     # choose closed-loop gains
    #     if key == ('k'):
    #         cl_gain_1 = input('Enter a closed loop gain for motor 1: ')
    #     if key == ('K'):
    #         cl_gain_2 = input('Enter a closed loop gain for motor 2: ')
            
    #     # choose velocity set point 
    #     if key == ('s'):
    #         vel_set_1 = input('Enter a velocity setpoint for motor 1: ')
    #     if key == ('S'):
    #         vel_set_2 = input('Enter a velocity setpoint for motor 2: ')
            
    #     # trigger step response and send data to be plott'd
    #     if key == ('r'):
    #         # step response f(n) mot 1
    #         pass
    #     if key == ('R'):
    #         # step response f(n) mot 2
    #         pass

    #     # set open loop again
    #     if key == 'o':
    #         loop_type = 1
    #     if key == 'O'
    #         loop_type = 1
