'''
    @name
    @brief
    @author
'''

import controls
from controls_gen import flags
import imu_driver as imu

def obj_hit_gen():
    state       = 'S0_WAIT'
    total_dist  = 0

    while True:
        if state == 'S0_WAIT':
            value = controls.switch()
            # check if hit
            if value == 1:
                controls.stop()
                print('OBJECT HIT')
                state = 'S1_HIT'
                flags['OBJ'] = True
        
        if state == 'S1_HIT':
            state = '90_RIGHT'

        if state == '90_RIGHT':
            ang = imu.imu_obj.euler()[0]
            controls.pivot_right(15)
            if 190 < ang < 194:
                controls.stop()
                state = '9IN_FOR'
                total_dist  = 0
            else:
                continue
        
        if state == '9IN_FOR':
            # get current distance and add tot total
            controls.forward(18, 15)
            total_dist += flags['CUR_DIST']
            print(total_dist)
            # check if travel complete
            if total_dist > 4.5:
                ref_ang = imu.imu_obj.euler()[0]
                controls.stop()
                state = '90_LEFT'
                total_dist = 0

        if state == '90_LEFT':
            ang = imu.imu_obj.euler()[0]
            print(ang)
            controls.pivot_left(25)
            if  ang < 35:
                controls.stop()
                state= '18IN_FOR'
            else:
                continue

        if state == '18IN_FOR':
            # get current distance and add tot total
            controls.forward(18, 15)
            total_dist      += flags['CUR_DIST']
            print(total_dist)
            # check if travel complete
            if total_dist > 9:
                controls.stop()
                state = '90_LEFT_2'
                total_dist = 0
        
        if state == '90_LEFT_2':
            print('turn 90 left')
            ang = imu.imu_obj.euler()[0]
            controls.pivot_left(25)
            if 518 < ang < 522:
                controls.stop()
                #state = '9IN_FOR_2'
            else:
                continue
        
        if state == '9IN_FOR_2':
            print('move 9 in forward')
            # get current distance and add tot total
            controls.forward(18, 15)
            current_dist    = .5 * ( flags['R_DIST'] + flags['L_DIST'])
            total_dist      += current_dist
            # check if travel complete
            if total_dist > 9:
                controls.stop()
                state = '90_RIGHT_2'
                total_dist = 0

        if state == '90_RIGHT_2':
            print('turn 90 right')
            ang = imu.imu_obj.euler()[0]
            controls.pivot_right(25)
            if ang < 35:
                controls.stop()
                state = 'DONE'
            else:
                continue
        
        if state == 'DONE':
            print('object avoided')
            flags['OBJ'] = False
            state == 'S0_WAIT'

        yield(state)