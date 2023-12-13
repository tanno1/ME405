'''
    @name
    @brief
    @author
'''

import controls
from controls_gen import flags
import imu_driver as imu
total_deg = 640

def normalize_angle(ang, ang_ref):
    diff =(ang - ang_ref) % total_deg
    if diff > total_deg / 2:
        diff -= total_deg
    return diff

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
            state   = '90_RIGHT'
            ang_ref = imu.imu_obj.euler()[0]
            print('ang_ref')

        if state == '90_RIGHT':
            ang = imu.imu_obj.euler()[0]
            controls.pivot_right(15)
            diff = normalize_angle(ang, ang_ref)
            if abs(diff) >= 160:
                controls.stop()
                state = '9IN_FOR'
                total_dist  = 0
            else:
                continue
        
        if state == '9IN_FOR':
            # get current distance and add tot total
            controls.forward(17, 15)
            total_dist += flags['CUR_DIST']
            print(total_dist)
            # check if travel complete
            if total_dist > 6:
                controls.stop()
                state = '90_LEFT'
                total_dist = 0
                ang_ref = imu.imu_obj.euler()[0]

        if state == '90_LEFT':
            ang = imu.imu_obj.euler()[0]
            controls.pivot_left(15)
            diff = normalize_angle(ang, ang_ref)
            print(diff)
            if abs(diff) >= 160:
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
            if total_dist > 12:
                controls.stop()
                state = '90_LEFT_2'
                total_dist = 0
                ang_ref = imu.imu_obj.euler()[0]
        
        if state == '90_LEFT_2':
            ang = imu.imu_obj.euler()[0]
            controls.pivot_left(15)
            diff = normalize_angle(ang, ang_ref)
            if abs(diff) >= 150:
                controls.stop()
                state = '9IN_FOR_2'
                total_dist = 0
            else:
                continue
        
        if state == '9IN_FOR_2':
            # get current distance and add tot total
            controls.forward(17, 15)
            total_dist      += flags['CUR_DIST']
            # check if travel complete
            if total_dist > 6:
                controls.stop()
                state = '90_RIGHT_2'
                total_dist = 0
                ang_ref = imu.imu_obj.euler()[0]

        if state == '90_RIGHT_2':
            ang = imu.imu_obj.euler()[0]
            controls.pivot_right(15)
            diff = normalize_angle(ang, ang_ref)
            if abs(diff) >= 160:
                controls.stop()
                state = 'DONE'
            else:
                continue
        
        if state == 'DONE':
            print('object avoided')
            flags['OBJ'] = False
            state = 'S0_WAIT'

        yield(state)