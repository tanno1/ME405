'''
    @file               main.py
    @brief              runs scheduled tasks on the nucleo board. each task is implemented as a generator function. the other necessary files to run this main are encoder.py, motor_class_main.py, ui.py, and closedloop.py
    @author             noah tanner, kosimo tonn
    @date               october 8th, 2023
'''

# imports
import cotask as cotask, pyb
import motor_class as motor, encoder_class as encoder, closed_loop as cl, ui as ui

# task definitions
class motor_controller_class:
    '''!@name           motor controller class
        @brief          creates a motor controller to be used in a generative task
    '''
    def __init__(self, encoder_1: encoder.Encoder, encoder_2: encoder.Encoder, driver_1: motor.L6206, driver_2: motor.L6206, collector_1: encoder.collector, collector_2: encoder.collector, flags: dict) -> None:
        self.encoder_1      = encoder_1
        self.encoder_2      = encoder_2
        self.driver_1       = driver_1
        self.driver_2       = driver_2
        self.collector_1    = collector_1
        self.collector_2    = collector_2
        self.flags          = flags
        self.duty_1         = 0
        self.duty_1         = 0
        self.kp_1           = 0
        self.kp_2           = 0
        self.vel_ref_1      = 0
        self.vel_ref_2      = 0

    def run(self):
        if ui.IS_FLAGS['DUTY_FLG1'] and ui.IS_FLAGS['VAL_DONE']:
            self.duty = ['VALUE']
            self.driver_1.set_duty(ui.IS_FLAGS['VALUE'])

        if ui.IS_FLAGS['DUTY_FLG2'] and ui.IS_FLAGS['VAL_DONE']:
            self.driver_1.set_duty(ui.IS_FLAGS['VALUE'])

        if ui.IS_FLAGS['DATA_FLG1']:
            if self.duty == 0:
                print('Duty cycle for motor 1 is set at 0, change then try again')
            self.collector_1.start(ui.IS_FLAGS['VALUE'], 2)

        if ui.IS_FLAGS['DATA_FLG2']:
            if self.duty == 0:
                print('Duty cycle for motor 2 is set at 0, change then try again')
            self.collector_2.start(ui.IS_FLAGS['VALUE'], 2)
         
        if ui.IS_FLAGS['CL_FLG1']:
            self.cl_loop_1 = cl.closed_loop(self.encoder_1, self.vel_ref_1, self.kp_2)
            while ui.IS_FLAGS['CL_FLG1']:
                self.new_duty = self.cl_loop_1.closed_loop()
                self.driver_1.set_duty(self.new_duty)

        if ui.IS_FLAGS['CL_FLG2']:
            self.cl_loop_2 = cl.closed_loop(self.encoder_2, self.vel_ref_2, self.kp_2)
            while ui.IS_FLAGS['CL_FLG2']:
                self.new_duty = self.cl_loop_2.closed_loop()
                self.driver_2.set_duty(self.new_duty)

        if ui.IS_FLAGS['K_FLG1'] and ui.IS_FLAGS['CL_FLG1'] and ui.IS_FLAGS['VAL_DONE']:
            self.kp_1 = ui.IS_FLAGS['VALUE']
            self.cl_loop_1 = cl.closed_loop(self.encoder_1, self.vel_ref_1, self.kp_1)

        if ui.IS_FLAGS['K_FLG2'] and ui.IS_FLAGS['CL_FLG2'] and ui.IS_FLAGS['VAL_DONE']:
            self.kp_2 = ui.IS_FLAGS['VALUE']
            self.cl_loop_2 = cl.closed_loop(self.encoder_2, self.vel_ref_2, self.kp_2)

        if ui.IS_FLAGS['VEL_FLG1'] and ui.IS_FLAGS['VAL_DONE']:
            self.vel_ref_1 = ui.IS_FLAGS['VALUE']
            self.cl_loop_1 = cl.closed_loop(self.encoder_1, self.vel_ref_1, self.kp_1)

        if ui.IS_FLAGS['VEL_FLG2'] and ui.IS_FLAGS['VAL_DONE']:
            self.vel_ref_2 = ui.IS_FLAGS['VALUE']
            self.cl_loop_2 = cl.closed_loop(self.encoder_2, self.vel_ref_2, self.kp_2)

def motor_controller_gen():
    while True:
        motor_controller = motor_controller_class(encoder.encoder_1, encoder.encoder_2, motor.mot_A, motor.mot_B, encoder.collector_1, encoder.collector_2, ui.IS_FLAGS)
        motor_controller.run()

def ui_gen():
    ui.UiTaskGen()
        
def export_gen():
    pass

# create task objects
cl_task         = cotask.Task( motor_controller_gen, "cl task", priority = 2, period = .001 )
ui_task         = cotask.Task( ui_gen, "ui task", priority = 0, period = .001 )
#export_task     = cotask.task( export_gen, "export task", priority = 0, period = .001)