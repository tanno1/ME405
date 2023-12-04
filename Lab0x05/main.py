import cotask
import imu_driver as imu
import ui_gen as ui
import controls

if __name__ == '__main__':

    imu_gen             = imu.imu_gen(imu.imu_obj)

    # create task objects
    ui_task             = cotask.Task(ui.ui_gen, "ui", priority = 2, period = 4, profile = True, trace = False)
    imu_task            = cotask.Task(imu_gen.run_gen, "imu", priority = 1, period = 4, profile = True, trace = False)
    controls_task       = 

    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            print("Stopped running")
            break
    
    print('\n' + str (cotask.task_list))
    print(controls_task.get_trace())
    print('')

    print('Program Terminated')