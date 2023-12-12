'''
    @name               main.py
    @brief              task scheduler for term project
    @author             tanner, noah
'''
import cotask
import pyb
import controls_gen
import obj_gen
import uos
import imu_driver as imu
import time

# call coefficient data
try:
    uos.stat('cal_coeff.txt')
    print('Calibration file found.')
    recal = 0

except OSError as e:
    if e.args[0] == 2:
        print('No calibration coefficient file found. Recalibrating...')
        recal = 1

if recal == 1:
    imu.calibrate(imu.imu_obj)

    print("Writing coefficients to new file \'cal_coeff.txt\'")
    acc_off, mag_off, gyr_off, rad_off = imu.imu_obj.get_cal_coeff()
    total_list = acc_off + mag_off + gyr_off + rad_off

    with open('cal_coeff.txt', 'w') as file:
    # Convert each element to a string and join them with commas
        line = ','.join(map(str, total_list))
        # Write the line to the file
        file.write(line)

elif recal == 0:
    file = 'cal_coeff.txt'
    with open(file, 'r') as file:
        cal_vals = file.readlines()
        cal_vals = cal_vals[0].split(',')
        print(dir(imu))

def main():

    # create task objects
    controls_task       = cotask.Task(controls_gen.line_follow_gen, "controls task", priority = 3, period = 10, profile = True, trace=False )
    obj_task            = cotask.Task(obj_gen.obj_hit_gen, "object task", priority = 2, period = 4, profile = True, trace=False  )


    # add tasks to task list
    cotask.task_list.append(controls_task)
    cotask.task_list.append(obj_task)

    print('program starting...')

    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            print('program exited')
            break

    print('\n' + str (cotask.task_list))
    #print(controls_task.get_trace())
    print(obj_task.get_trace())
    print('')

    print('Program Terminated')