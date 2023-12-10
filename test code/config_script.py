#!/usr/bin/env python3
import time
from gripper import open_gripper, close_gripper
from ev3movement import driveStraight, stop_motors, spin
from robot_controls import pid_control as pd

SPEED = 70

def receiver_function(distance: int) -> bool:
    try:
        #stop the robot and switch to ultrasound if the you cover 80% of distance
        stop_distance = 0.8 * distance
        driveStraight(SPEED, stop_distance)
        stop_motors()
        
        pd(5)
        open_gripper()
        driveStraight(30, 2)
        time.sleep(2)
        close_gripper()
        

        return True
    except Exception as e:
        # Handle any exceptions that might occur during the movement
        # print(f"Error during movement: {e}")
        return False
    
if __name__ == "__main__":
    distance = 60
    print(receiver_function(distance=distance))