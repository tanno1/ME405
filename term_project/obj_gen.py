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
                ang_ref = imu.imu_obj.euler()[0]
                print(f'ANG REF: {ang_ref}')
                state = 'S1_HIT'
                flags['OBJ'] = True
        
        if state == 'S1_HIT':
            substate = '90_RIGHT'

            if substate == '90_RIGHT':
                ang = imu.imu_obj.euler()[0]
                print(ang)
                controls.pivot_right(15)
                if ang < (ang_ref + 160):
                    continue
                else:
                    controls.stop()
                    substate = '9IN_FOR'
            
            if substate == '9IN_FOR':
                # get current distance and add tot total
                controls.forward(25, 25)
                current_dist    = .5 * ( flags['R_DIST'] + flags['L_DIST'])
                total_dist      += current_dist
                # check if travel complete
                if total_dist > 9:
                    controls.stop()
                    substate = '90_LEFT'
                    total_dist = 0

            if substate == '90_LEFT':
                ang = imu.imu_obj.euler()[0]
                ang_og = imu.imu_obj.euler()[0]
                controls.pivot_right(25)
                if ang < (ang_ref - 160):
                    continue
                else:
                    controls.stop()
                    substate = '18IN_FOR'

            if substate == '18IN_FOR':
                # get current distance and add tot total
                controls.forward(25, 25)
                current_dist    = .5 * ( flags['R_DIST'] + flags['L_DIST'])
                total_dist      += current_dist
                # check if travel complete
                if total_dist > 18:
                    controls.stop()
                    substate = '90_LEFT_2'
                    total_dist = 0
            
            if substate == '90_LEFT_2':
                ang_og = imu.imu_obj.euler()[0]
                ang = imu.imu_obj.euler()[0]
                controls.pivot_right(25)
                if ang < (ang_ref - 160):
                    continue
                else:
                    controls.stop()
                    substate = '9IN_FOR_2'
            
            if substate == '9IN_FOR_2':
                # get current distance and add tot total
                controls.forward(25, 25)
                current_dist    = .5 * ( flags['R_DIST'] + flags['L_DIST'])
                total_dist      += current_dist
                # check if travel complete
                if total_dist > 9:
                    controls.stop()
                    substate = '90_RIGHT_2'
                    total_dist = 0

            if substate == '90_RIGHT_2':
                ang_og = imu.imu_obj.euler()[0]
                ang = imu.imu_obj.euler()[0]
                controls.pivot_right(25)
                if ang < (ang_ref + 160):
                    continue
                else:
                    controls.stop()
                    substate = 'DONE'
            
            if substate == 'DONE':
                print('object avoided')
                flags['OBJ'] = False
                state == 'S0_WAIT'

        yield(state)