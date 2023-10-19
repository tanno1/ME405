'''
    @file               ui.py
    @brief              class file to control the keyboard input from users and implement results as a generator task function inside of main.py
    @author             noah tanner, kosimo tonn
    @date               october 8th, 2023
'''

# Imports
import ui.py as ui, encoder_class.py as encoder, motor_class.py as motor

# variables
valid_commands = ['z', 'Z', 'p', 'P', 'v', 'V', 'm', 'M', 'g', 'G', 'c', 'C', 'k', 'K', 's', 'S', 'r', 'R', 'o', 'O']
# set loop type [ 1 = open, 2 = closed ]
loop_type = 1

#Main
while True:
    # wait for valid command to be entered
    while len(key) != 1 or key not in valid_commands
        key = input('Enter a command: ')
        print('Invalid command, try again.')

    #Zero Encoders
    elif key == ('z'):
        encoder.encoder_1.zero()
        print('Position of encoder 1 zero\'d') 
    elif key == ('Z'):
        encoder.encoder_2.zero()
        print('Position of encoder 2 zero\'d')

    # print position
    elif key == ('p'):
        print('Position of encoder 1: {}'.format(encoder.encoder_1.current_position))
    elif key == ('p'):
        print('Position of encoder 2: {}'.format(encoder.encoder_2.current_position)) 

    # print Velocity     
    if key == ('v'):
        print('Velocity of encoder 1: {} rad/s or {} rpm'.format(encoder.encoder_1.velocity['rad/s'], encoder.encoder_1.velocity['rpm']))
    if key == ('V'):
        print('Velocity of encoder 2: {} rad/s or {} rpm'.format(encoder.encoder_2.velocity['rad/s'], encoder.encoder_2.velocity['rpm']))
      
    # enter a duty cycle   
    if key == ('m'):
        while duty_cycle_1 not in range(-100, 101) or duty_cycle_1 not float:
            duty_cycle_1 = input('Enter a duty cycle for motor 1: ')
            print('Enter a valid integer from -100 to 100')
        motor.mot_A.set_duty(duty_cycle_1)
        print('Duty cycle for motor 1 set to {}'.format(duty_cycle_1))

    if key == ('M'):
        while duty_cycle_2 not in range(-100, 101) or duty_cycle_2 not float:
            duty_cycle_2 = input('Enter a duty cycle for motor 2: ')
            print('Enter a valid integer from -100 to 100')
        motor.mot_B.set_duty(duty_cycle_2)
        print('Duty cycle for motor 2 set to {}'.format(duty_cycle_2))
        
    # collect speed and position for 30 seconds
    if key == ('g'):
        encoder.encoder_1.start(duty_cycle_1, 2)
        print('Collecting encoder 1 speed and position')
        while encoder.encoder_1.idx != 29999:
            time.sleep(1)
            print('Collecting data...')

    if key == ('G'):
        encoder.encoder_2.start(duty_cycle_2, 2)
        print('Collecting encoder 2 speed and position')
        while encoder.encoder_2.idx != 29999:
            time.sleep(1)
            print('Collecting data...')

        
    # Switch to Closed-Loop Mode    
    if key == ('C' or 'c'):
        loop_type = 2
    
    # skip these commands if loop is open
    if loop_type = 2:  
        # choose closed-loop gains
        if key == ('k'):
            cl_gain_1 = input('Enter a closed loop gain for motor 1: ')
        if key == ('K'):
            cl_gain_2 = input('Enter a closed loop gain for motor 2: ')
            
        # choose velocity set point 
        if key == ('s'):
            vel_set_1 = input('Enter a velocity setpoint for motor 1: ')
        if key == ('S'):
            vel_set_2 = input('Enter a velocity setpoint for motor 2: ')
            
        # trigger step response and send data to be plott'd
        if key == ('r'):
            # step response f(n) mot 1
            pass
        if key == ('R'):
            # step response f(n) mot 2
            pass

        # set open loop again
        if key == 'o':
            loop_type = 1
        if key == 'O'
            loop_type = 1
