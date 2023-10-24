'''
    @file               main.py
    @brief              runs scheduled tasks on the nucleo board. each task is implemented as a generator function. the other necessary files to run this main are encoder.py, motor_class_main.py, ui.py, and closedloop.py
    @author             noah tanner, kosimo tonn
    @date               october 8th, 2023
'''

# imports
import cotask
from pyb import Pin, Timer, UART
import motor_class as motor
import encoder_class as encoder
import cl_gen as cl
import ui_gen as ui

if __name__ == '__main__':
    export_task             = 0

    motor_controller_task   = cl.motor_generator_class(encoder.enc_1, encoder.enc_2, motor.mot_A, motor.mot_B, encoder.collector_1, encoder.collector_2, ui.IS_FLAGS)

    # create task objects
    cl_task      = cotask.Task( motor_controller_task.run_gen, "cl task", priority = 1, period = 40 )
    ui_task      = cotask.Task( ui.ui_gen, "ui task", priority = 2, period = 40 )
    #export_task     = cotask.task( export_task, "export task", priority = 0, period = .001)
    cotask.task_list.append(cl_task)
    cotask.task_list.append(ui_task)

    ser = UART(2,115200)

    print('Program starting...')

    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            ser.write("Stopped running")
            break

    print('Program Terminated')