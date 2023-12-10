
'''
    @name                  lab4_main.py
    @brief                 lab4 main file for circle line following
    @author                tanner, noah
    @date                  november, 2023
'''

from pyb import Pin, ADC, Timer
import romi_driver as driver
import encoder_class as encoder
import imu_driver as imu
import time
from math import pi

# sensor array [ 3, 4, 5, 6, 7, 8, 9 ] with 3 being on left when romi faces forward

# setup sensor pins
P3          = Pin(Pin.cpu.A0, mode=Pin.IN)
P4          = Pin(Pin.cpu.A1, mode=Pin.IN)
P5          = Pin(Pin.cpu.A4, mode=Pin.IN)
P6          = Pin(Pin.cpu.B0, mode=Pin.IN)
P7          = Pin(Pin.cpu.A7, mode=Pin.IN)
P8          = Pin(Pin.cpu.A6, mode=Pin.IN)
P9          = Pin(Pin.cpu.A5, mode=Pin.IN)

# adc setup
adc3        = ADC(P3)
adc4        = ADC(P4)
adc5        = ADC(P5)
adc6        = ADC(P6)
adc7        = ADC(P7)
adc8        = ADC(P8)
adc9        = ADC(P9)

val_array   = [ 0, 0, 0, 0, 0, 0, 0 ]
adc_array   = [ adc3, adc4, adc5, adc6, adc7, adc8, adc9 ]

# calibration values:
white = [285.7, 279.9, 276.7, 272.9, 292.4, 1836.1, 4059.3]
black = [3274.6, 3094.8, 2866.8, 2749.4, 2084.8, 1858.6, 4059.2]


def calibrate(color):
    cal_array   = [ 0, 0, 0, 0, 0, 0, 0 ]
    idx         = 0
    iter        = 10

    if color == 'white':
        while iter > 0:
            while idx < len(cal_array):
                cal_array[idx] += adc_array[idx].read()
                idx += 1
            time.sleep(1)
            idx = 0
            iter -= 1
            print(cal_array)

        white_cal_array = [ ( val / 10 ) for val in cal_array ]
        return white_cal_array

    if color == 'black':
        while iter > 0:
            while idx < len(cal_array):
                cal_array[idx] += adc_array[idx].read()
                idx += 1
            time.sleep(1)
            idx = 0
            iter -= 1
            print(cal_array)

        black_cal_array = [ ( val / 10 ) for val in cal_array ]
        return black_cal_array

def read():
    idx = 0
    while idx < len(val_array):
        val_array[idx] = adc_array[idx].read()
        idx += 1
    
    return val_array

def calc_centroid():
    sensor_vals     = read()
    weighted_sum    = sum(i * val for i, val in enumerate(sensor_vals))
    total_sum       = sum(sensor_vals)
    centroid        = weighted_sum / total_sum

    return centroid

def forward(speed):
    right.set_duty(speed, 1)
    left.set_duty(speed, 1)
    right.enable()
    left.enable()

def turn_right(left_speed, right_speed):
    left.set_duty(left_speed, 0)
    right.set_duty(right_speed, 0)
    left.enable()
    right.disable()

def turn_left(left_speed, right_speed):
    left.set_duty(left_speed, 0)
    right.set_duty(right_speed, 0)
    right.enable()
    left.disable()

def pivot_right(speed):
    left.set_duty(speed, 1)
    right.set_duty(speed, 0)
    left.enable()
    right.enable()

def pivot_left(speed):
    left.set_duty(speed, 0)
    right.set_duty(speed, 1)
    left.enable()
    right.enable()

def stop():
    right.disable()
    left.disable()

cpr         = 1440          # encoder count per revolution of romi wheel
wheel_dia   = 2.83          # romi wheel diameter in inches
wheel_circ  = 2.83 * pi

def calc_distance(counts):
    rev  = counts / cpr
    dist = rev * wheel_circ
    return dist 

# initialize total distance variables
dist_left = 0
dist_right = 0

def loop(threshold, base_speed, kp, ki, kd):
    while True:
        sensor_vals     = read()
        centroid        = calc_centroid()
        reference_pt    = len(sensor_vals) / 2
        pid_output      = pid_controller(centroid, reference_pt, kp, ki, kd)
        new_left        = base_speed + pid_output
        new_right       = base_speed - pid_output

        if centroid < reference_pt - threshold:
            turn_left(new_left, new_right)
            print('turned left)')
        elif centroid > reference_pt + threshold:
            turn_right(new_left, new_right)
            print('turned right')
        else:
            forward()

def loop_and_stop(threshold, base_speed, kp, ki, kd):
    total_dist = 0
    while total_dist < 75.36:
        enc_right.update()
        enc_left.update()
        dist_left   = calc_distance(-enc_left.total_position)
        dist_right  = calc_distance(-enc_right.total_position)
        total_dist  = .5 * (dist_left + dist_right)
        print(f"Distances [ L: {dist_left}, R: {dist_right}, Total: {total_dist}]")
        sensor_vals     = read()
        centroid        = calc_centroid()
        reference_pt    = len(sensor_vals) / 2
        pid_output      = pid_controller(centroid, reference_pt, kp, ki, kd)
        new_left        = base_speed + pid_output
        new_right       = base_speed - pid_output

        # check encoder values to determine when to stop

        if centroid < reference_pt - threshold:
            turn_left(new_left, new_right)
            print('turned left)')
        elif centroid > reference_pt + threshold:
            turn_right(new_left, new_right)
            print('turned right')
        else:
            forward()
    stop()
    print('arrived at the start')

def test_switch():
    val = switch_pin.value()
    print(val)

# initialize variables for pid controller
prev_error = 0
integral   = 0  

def pid_controller(centroid, reference_pt, kp, ki, kd):
    global integral, prev_error
    error       = reference_pt - centroid
    integral    += error
    derivative  = error - prev_error

    pid_res     = kp * error + ki * integral + kd * derivative
    prev_error  = error
    print(pid_res)
    return pid_res

def obstacle():
    # only enter this funciton when limit switch == 1
    ang = imu.imu_obj.euler[0]
    # 1. pivot 90 deg right
    pivot_right(25)
    while ang < (ang + 90):                 # check if CW rot coresponds to + 90 rot
        ang = imu.imu_obj.euler[0]
    stop()

    # 2. move 9" forward
    total_dist = 0
    forward(25)
    while total_dist < 9: 
        enc_right.update()
        enc_left.update()
        dist_left   = calc_distance(-enc_left.total_position)
        dist_right  = calc_distance(-enc_right.total_position)
        total_dist  = .5 * (dist_left + dist_right)
    stop()

    # 3. pivot 90 deg left
    ang = imu.imu_obj.euler[0]
    pivot_left(25)
    while ang < (ang - 90):                 # check if CCW rot coresponds to - 90 rot
        ang = imu.imu_obj.euler[0]
    stop()
    # 4. move 18" forward
    total_dist = 0
    forward(25)
    while total_dist < 18: 
        enc_right.update()
        enc_left.update()
        dist_left   = calc_distance(-enc_left.total_position)
        dist_right  = calc_distance(-enc_right.total_position)
        total_dist  = .5 * (dist_left + dist_right)
    stop()

    # 5. pivot 90 deg left
    ang = imu.imu_obj.euler[0]
    pivot_left(25)
    while ang < (ang - 90):                 # check if CCW rot coresponds to - 90 rot
        ang = imu.imu_obj.euler[0]
    stop()

    # 6. move 9" forward
    total_dist = 0
    forward(25)
    while total_dist < 9: 
        enc_right.update()
        enc_left.update()
        dist_left   = calc_distance(-enc_left.total_position)
        dist_right  = calc_distance(-enc_right.total_position)
        total_dist  = .5 * (dist_left + dist_right)
    stop()

    # 7. pivot 90 deg right
    ang = imu.imu_obj.euler[0]
    pivot_right(25)
    while ang < (ang + 90):                 # check if CW rot coresponds to + 90 rot
        ang = imu.imu_obj.euler[0]
    stop()

# left driver
tim_left        = Timer(4, freq = 20_000)
pwm_left_pin    = Pin(Pin.cpu.B6, mode=Pin.OUT_PP)
pwm_left        = tim_left.channel(1, pin = pwm_left_pin, mode=Timer.PWM)
dir_left_pin    = Pin(Pin.cpu.B9, mode=Pin.OUT_PP)
en_left_pin     = Pin(Pin.cpu.B7, mode=Pin.OUT_PP)
left            = driver.romi_driver(tim_left, pwm_left, dir_left_pin, en_left_pin)

# right driver
tim_right       = Timer(8, freq = 20_000)
pwm_right_pin   = Pin(Pin.cpu.C9)
dir_right_pin   = Pin(Pin.cpu.C8, mode=Pin.OUT_PP)
en_right_pin    = Pin(Pin.cpu.C7, mode=Pin.OUT_PP)
# configure channels 2, 3, 4
pwm_right       = tim_right.channel(4, pin = pwm_right_pin, mode=Timer.PWM)
right           = driver.romi_driver(tim_right, pwm_right, dir_right_pin, en_right_pin)

# encoder left
ps          = 0
ar          = 1000
l_pin_cha   = Pin(Pin.cpu.B4, mode=Pin.OUT_PP)                          # encoder 1, channel a pin
l_pin_chb   = Pin(Pin.cpu.B5, mode=Pin.OUT_PP)                          # encoder 1, channel b pin
tim_left_3  = Timer(3, period = ar, prescaler = ps)                     # encoder 1 timer
l_cha       = tim_left_3.channel(1, pin=l_pin_cha, mode=Timer.ENC_AB)  
l_chb       = tim_left_3.channel(2, pin=l_pin_chb, mode=Timer.ENC_AB)  
enc_right   = encoder.Encoder(tim_left_3, l_cha, l_chb, ar, ps)         # encoder 1 instance

# encoder right
r_pin_cha   = Pin(Pin.cpu.A8, mode=Pin.OUT_PP)                          # encoder 1, channel a pin
r_pin_chb   = Pin(Pin.cpu.A9, mode=Pin.OUT_PP)                          # encoder 1, channel b pin
tim_left_1  = Timer(1, period = ar, prescaler = ps)                     # encoder 1 timer
r_cha       = tim_left_1.channel(1, pin=r_pin_cha, mode=Timer.ENC_AB)  
r_chb       = tim_left_1.channel(2, pin=r_pin_chb, mode=Timer.ENC_AB)  
enc_left    = encoder.Encoder(tim_left_1, r_cha, r_chb, ar, ps)         # encoder 1 instance

# limit switch
switch_pin  = Pin(Pin.cpu.C0, mode=Pin.IN, pull=Pin.PULL_UP)

# set motor speed and direction ( 0 = forward, 1 = reverse )
left.disable()
right.disable()
# VALUES from testing: Threshold: 0.1, P: -, I: -, D: -