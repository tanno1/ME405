'''
    @file               main.py
    @brief              runs scheduled tasks on the nucleo board. each task is implemented as a generator function. the other necessary files to run this main are encoder.py, motor_class_main.py, ui.py, and closedloop.py
    @author             noah tanner, kosimo tonn
    @date               october 8th, 2023
'''

# imports
import cotask as cotask
from pyb import Pin, Timer
import motor_class as motor, encoder_class as encoder, closed_loop as cl, ui_gen as ui

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

# def motor_controller_gen():
#     while True:
#         motor_controller = motor_controller_class(encoder.encoder_1, encoder.encoder_2, motor.mot_A, motor.mot_B, encoder.collector_1, encoder.collector_2, ui.IS_FLAGS)
#         motor_controller.run()

# def ui_gen():
#     ui.ui_gen()
        
# def export_gen():
#     pass

def main():
    
    motor_controller_task   = motor_controller_class.run()
    ui_task                 = ui.ui_gen()
    export_task             = 0

    # motor a
    tim_A       = Timer(3, freq = 20_000)                               # timer3 for motor A
    EN_a        = Pin(Pin.cpu.A10, mode=Pin.OUT_PP)                     # motA active high-enable
    IN1_a       = Pin(Pin.cpu.B4, mode=Pin.OUT_PP)                      # motA control pin 1
    IN2_a       = Pin(Pin.cpu.B5, mode=Pin.OUT_PP)                      # motA control pin 2
    mot_A       = motor.L6206(tim_A, EN_a, IN1_a, IN2_a)                # initialize motor A object
    # encoder mot_a
    ps          = 0
    ar          = 1000
    cha_pin_1   = Pin(Pin.cpu.C7, mode=Pin.OUT_PP)                      # encoder 1, channel a pin
    chb_pin_1   = Pin(Pin.cpu.C6, mode=Pin.OUT_PP)                      # encoder 1, channel b pin
    tim_a_8     = Timer(8, period = ar, prescaler = ps)                 # encoder 1 timer
    cha_1       = tim_a_8.channel(1, pin=cha_pin_1, mode=Timer.ENC_AB)  #
    chb_1       = tim_a_8.channel(2, pin=chb_pin_1, mode=Timer.ENC_AB)  #
    enc_1       = encoder.Encoder(tim_a_8, cha_1, chb_1, ar, ps)        # encoder 1 instance
    # collector mot_a
    tim_6       = Timer(6, freq = 1000)                                 # timer for datat collection   
    collector_1 = encoder.collector(tim_6, enc_1, mot_A)                # collector instance 

    # motor b
    tim_B       = Timer(2, freq = 20_000)                               # timer2 for motor B
    EN_b        = Pin(Pin.cpu.C1, mode=Pin.OUT_PP)                      # motB active high-enable
    IN1_b       = Pin(Pin.cpu.A0, mode=Pin.OUT_PP)                      # motB control pin 1
    IN2_b       = Pin(Pin.cpu.A1, mode=Pin.OUT_PP)                      # motB control pin 2
    mot_B       = motor.L6206(tim_B, EN_b, IN1_b, IN2_b)                # initialize motor B object
    # encoder mot_b
    cha_pin_2   = Pin(Pin.cpu.B6, mode=Pin.OUT_PP)                      # encoder 1, channel a pin
    chb_pin_2   = Pin(Pin.cpu.B7, mode=Pin.OUT_PP)                      # encoder 1, channel b pin
    tim_a_4     = Timer(4, period = ar, prescaler = ps)                 # encoder 1 timer
    cha_2       = tim_a_4.channel(1, pin=cha_pin_2, mode=Timer.ENC_AB)  #
    chb_2       = tim_a_4.channel(2, pin=chb_pin_2, mode=Timer.ENC_AB)  #
    enc_2       = encoder.Encoder(tim_a_8, cha_2, chb_2, ar, ps)        # encoder 1 instance
    # collector mot_b
    tim_7       = Timer(7, freq = 1000)                                 # timer for datat collection   
    collector_2 = encoder.collector(tim_7, enc_2, mot_B)                # collector instance 

    while True:
        # create task objects
        cl_task         = cotask.Task( motor_controller_task, "cl task", priority = 2, period = .001 )
        ui_task         = cotask.Task( ui_task, "ui task", priority = 0, period = .001 )
        #export_task     = cotask.task( export_task, "export task", priority = 0, period = .001)

        try:
            # w/ above task objects, schedule them!
            pass

        except KeyboardInterrupt:
            break

    print('Program Terminated')

if __name__ == '__main__':
    main()