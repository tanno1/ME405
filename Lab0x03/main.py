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
from ui_gen import IS_FLAGS

if __name__ == '__main__':

    #v DOUBLE CHECK v
    export_task             = 0

    # # motor a
    # tim_A       = Timer(3, freq = 20_000)                               # timer3 for motor A
    # EN_a        = Pin(Pin.cpu.A10, mode=Pin.OUT_PP)                     # motA active high-enable
    # IN1_a       = Pin(Pin.cpu.B4, mode=Pin.OUT_PP)                      # motA control pin 1
    # IN2_a       = Pin(Pin.cpu.B5, mode=Pin.OUT_PP)                      # motA control pin 2
    # mot_A       = motor.L6206(tim_A, EN_a, IN1_a, IN2_a)                # initialize motor A object
    # # encoder mot_a
    # ps          = 0
    # ar          = 1000
    # cha_pin_1   = Pin(Pin.cpu.C7, mode=Pin.OUT_PP)                      # encoder 1, channel a pin
    # chb_pin_1   = Pin(Pin.cpu.C6, mode=Pin.OUT_PP)                      # encoder 1, channel b pin
    # tim_a_8     = Timer(8, period = ar, prescaler = ps)                 # encoder 1 timer
    # cha_1       = tim_a_8.channel(1, pin=cha_pin_1, mode=Timer.ENC_AB)  #
    # chb_1       = tim_a_8.channel(2, pin=chb_pin_1, mode=Timer.ENC_AB)  #
    # enc_1       = encoder.Encoder(tim_a_8, cha_1, chb_1, ar, ps)        # encoder 1 instance
    # # collector mot_a
    # tim_6       = Timer(6, freq = 1000)                                 # timer for datat collection   
    # collector_1 = encoder.collector(tim_6, enc_1, mot_A)                # collector instance 

    # # motor b
    # tim_B       = Timer(2, freq = 20_000)                               # timer2 for motor B
    # EN_b        = Pin(Pin.cpu.C1, mode=Pin.OUT_PP)                      # motB active high-enable
    # IN1_b       = Pin(Pin.cpu.A0, mode=Pin.OUT_PP)                      # motB control pin 1
    # IN2_b       = Pin(Pin.cpu.A1, mode=Pin.OUT_PP)                      # motB control pin 2
    # mot_B       = motor.L6206(tim_B, EN_b, IN1_b, IN2_b)                # initialize motor B object
    # # encoder mot_b
    # cha_pin_2   = Pin(Pin.cpu.B6, mode=Pin.OUT_PP)                      # encoder 1, channel a pin
    # chb_pin_2   = Pin(Pin.cpu.B7, mode=Pin.OUT_PP)                      # encoder 1, channel b pin
    # tim_a_4     = Timer(4, period = ar, prescaler = ps)                 # encoder 1 timer
    # cha_2       = tim_a_4.channel(1, pin=cha_pin_2, mode=Timer.ENC_AB)  #
    # chb_2       = tim_a_4.channel(2, pin=chb_pin_2, mode=Timer.ENC_AB)  #
    # enc_2       = encoder.Encoder(tim_a_8, cha_2, chb_2, ar, ps)        # encoder 1 instance
    # # collector mot_b
    # tim_7       = Timer(7, freq = 1000)                                 # timer for datat collection   
    # collector_2 = encoder.collector(tim_7, enc_2, mot_B)                # collector instance 

    motor_controller_task   = cl.motor_generator_class(encoder.enc_1, encoder.enc_2, motor.mot_A, motor.mot_B, encoder.collector_1, encoder.collector_2, IS_FLAGS)

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