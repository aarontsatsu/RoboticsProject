#!/usr/bin/env python3

from ev3dev2.motor import MediumMotor, OUTPUT_A
from time import sleep

# Connect the medium motor to port A
gripper_motor = MediumMotor(OUTPUT_A)

def close_gripper():
    gripper_motor.on_for_seconds(speed=-50, seconds=2) 
    if gripper_motor.is_stalled: 
        gripper_motor.stop()
    gripper_motor.stop()

def open_gripper():
    gripper_motor.on_for_seconds(speed=50, seconds=2)  
    gripper_motor.stop()

