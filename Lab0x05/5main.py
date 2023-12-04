'''
    @file               main.py
    @brief              runs scheduled tasks on the nucleo board. each task is implemented as a generator function. the other necessary files to run this main are encoder.py, motor_class_main.py, ui.py, and closedloop.py
    @author             noah tanner, kosimo tonn
    @date               october 8th, 2023
'''

# imports
import cotask
import imu_driver as imu
import cl_gen as cl
import ui_gen as ui
import controls
import uos

if __name__ == '__main__':

    motor_controller_task   = cl.motor_generator_class(controls.enc_left, controls.enc_right, controls.left, controls.right, imu.imu_obj, ui.IS_FLAGS)

    # create task objects
    motor_task      = cotask.Task( motor_controller_task.run_gen, "cl task", priority = 1, period = 4, profile=True, trace=False )
    ui_task         = cotask.Task( ui.ui_gen, "ui task", priority = 2, period = 4, profile=True, trace=False )
    cotask.task_list.append(motor_task)
    cotask.task_list.append(ui_task)


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
            print(cal_vals)
    
        imu.imu_obj.write_cal_coeff(cal_vals)
        print('Calibration coefficients from file written to IMU')
    
    print('Program starting...')

    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            print("Stopped running")
            break
    
    print('\n' + str (cotask.task_list))
    print(motor_task.get_trace())
    print('')

    print('Program Terminated')