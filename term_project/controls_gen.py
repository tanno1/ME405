'''
    @name
    @brief
    @author
'''

import controls

flags       = { 'STRAIGHT': False,
                    'TURN':     False,
                    'OBJ':      False,
                    'R_DIST':   0,
                    'L_DIST':   0       }

def line_follow_gen():
    threshold   = .3
    base_speed  = 25
    kp          = 3
    ki          = .02
    kd          = .4
    state       = 'S0_LOOP'

    while True:

        if state == 'S0_LOOP':
            if flags['OBJ'] != True:
                # calculate distance traveled since last movement
                controls.enc_right.update()
                controls.enc_left.update()
                flags['L_DIST'] = controls.calc_distance(-controls.enc_left.total_position)
                flags['R_DIST'] = controls.calc_distance(-controls.enc_right.total_position)

                # get current sensor reading and determine what to do
                sensor_vals     = controls.read()
                if all(value < 500 for value in sensor_vals):
                    controls.forward(base_speed, base_speed)
                    print('abyss detected')
                else:
                    centroid        = controls.calc_centroid()
                    reference_pt    = len(sensor_vals) / 2
                    pid_output      = controls.pid_controller(centroid, reference_pt, kp, ki, kd)
                    new_left        = base_speed + pid_output
                    new_right       = base_speed - pid_output

                    if centroid < reference_pt - threshold:
                        controls.turn_left(new_left, new_right)
                        flags['TURN'] = True
                        #print('turned left')
                    elif centroid > reference_pt + threshold:
                        controls.turn_right(new_left, new_right)
                        flags['TURN'] = True
                        #print('turned right')
                    else:
                        controls.forward(new_left, new_right)
                        flags['STRAIGHT'] = True
                        #print('moved forward')

                #print(f'Left speed: {new_left}, Right speed: {new_right}, PID: {pid_output}')
            
            elif flags['OBJ'] == True:
                continue

        yield(state)