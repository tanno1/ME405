import cotask
import imu_driver as imu
import ui_gen as ui

if __name__ == '__main__':
    print('here')

    # create task objects
    ui_task             = cotask.Task(ui.ui_gen, "ui", priority = 2, period = 4, profile = True, trace = False)
    cotask.task_list.append(ui_task)

    file = 'cal_coeff.txt'
    try:
        with open(file, 'r') as file:
            cal_vals = file.readlines()
            cal_vals = cal_vals[0].split(',')
            print(cal_vals)
    except:
        print('no calibration coefficient file found')
        imu.calibrate(imu.imu_obj)
        imu.save_calibration(imu.imu_obj, 'cal_coeff.txt')
        imu.imu_obj.change_mode('NDOF')

    print('ui task initialized')
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            print("Stopped running")
            break
    
    print('\n' + str (cotask.task_list))
    print(ui_task.get_trace())
    print('')

    print('Program Terminated')