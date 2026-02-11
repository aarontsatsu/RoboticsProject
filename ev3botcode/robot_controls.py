#!/usr/bin/env python3

from ev3dev2.motor import OUTPUT_B, OUTPUT_C, MoveTank, SpeedDPS
from ev3dev2.sensor.lego import UltrasonicSensor
import time

c3 = UltrasonicSensor()
motors = MoveTank(OUTPUT_B, OUTPUT_C)

def pid_control(target):
    prev_error = target - c3.distance_centimeters
    KP, KD, KI, OFFSET = 0.5, 0.5, 0.1, 0
    error_change = 0  # Initialize error_change to 0
    error_integral = prev_error
    output = (KP * prev_error) + (KD * error_change) + (KI * error_integral) + OFFSET

    while True:
        new_distance = c3.distance_centimeters
        new_error = target - new_distance
        error_change = new_error - prev_error
        error_integral += new_error
        prev_error = new_error
        output = (KP * prev_error) + (KD * error_change) + (KI * error_integral) + OFFSET

        # Adjust the following condition to stop the motors when the target distance is reached
        if abs(new_error) < 6.0:  # You can adjust the threshold (0.5 cm in this case)
            motors.off(brake=True)
            break

        if output > 100.0:
            output = 100.0
        elif output < -100.0:
            output = -100.0
        else:
            if prev_error > 0:
                motors.on(left_speed=SpeedDPS(output), right_speed=SpeedDPS(output))
            elif prev_error < 0:
                motors.on(left_speed=SpeedDPS(-output), right_speed=SpeedDPS(-output))
            else:
                motors.off(brake=True)

        time.sleep(0.1)
