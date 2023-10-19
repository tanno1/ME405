'''
    @file               main.py
    @brief              runs scheduled tasks on the nucleo board. each task is implemented as a generator function. the other necessary files to run this main are encoder.py, motor_class_main.py, ui.py, and closedloop.py
    @author             noah tanner, kosimo tonn
    @date               october 8th, 2023
'''

# imports
import cotask
import motor_class_main.py as mot_class, encoder.py as enc_class, closedloop.py as cl_class, ui.py as ui

# task definitions
def closedloop_task():
    while True:
        yield state
    pass

def ui_task():
    while True:
        yield state
    pass

# create task objects
cl_task         = cotask.task(closedloop_task, "cl task", priority = 2, period = .001)
ui_task         = cotask.task(ui_task, "ui task", priority = 0, period = .001)