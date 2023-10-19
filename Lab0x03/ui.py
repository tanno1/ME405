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
        print('Position of encoder 1 zero\'d') 
    elif key == ('Z'):
        print('Position of encoder 2 zero\'d')

    # print position
    elif key == ('p'):
        print('Position of encoder 1: {}'.format())
    elif key == ('p'):
        print('Position of encoder 2: {}'.format()) 

    # print Velocity     
    if key == ('v'):
        print('Velocity of encoder 1: {}'.format())
    if key == ('V'):
        print('Velocity of encoder 2: {}'.format())  
      
    # enter a duty cycle   
    if key == ('m'):
        duty_cycle_1 = input('Enter a duty cycle for motor 1: ')
    if key == ('M'):
        duty_cycle_2 = input('Enter a duty cycle for motor 2: ')
        
    # collect speed and position for 30 seconds
    if key == ('g'):
        # collect data functions
        pass
    if key == ('G'):
        # collect data functions
        pass
        
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
