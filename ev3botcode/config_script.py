#!/usr/bin/env python3
import time
from ev3gripper import open_gripper, close_gripper
from ev3movement import driveStraight, stop_motors, spin
from robot_controls import pid_control as pd

SPEED = 70

def receiver_function(type:str, distance: float) -> bool:
    
    if type == "obj":
        if distance > 80:
            distance = 60
        try:
            #stop the robot and switch to ultrasound if the you cover 80% of distance
            stop_distance = 0.8 * distance
            spin(175,30,'left')
            driveStraight(SPEED, stop_distance)
            stop_motors()
            pd(5)
            open_gripper()
            driveStraight(20, 7)
            time.sleep(2)
            close_gripper()
            return True
        except Exception as e:
            # Handle any exceptions that might occur during the movement
            # print(f"Error during movement: {e}")
            return False
    elif type == 'coll':
    
        try:
            
            # spin(180,30,'left')
            #stop the robot and switch to ultrasound if the you cover 80% of distance
            stop_distance = 0.8 * distance
            driveStraight(-SPEED, stop_distance)
            stop_motors()
            spin(180,30,'left')
            pd(5)
            open_gripper()
            time.sleep(2)
            driveStraight(SPEED, -15)
            close_gripper()
            spin(90,30,'left')
            return True
        except Exception as e:
            # Handle any exceptions that might occur during the movement
            # print(f"Error during movement: {e}")
            return False

        
# if __name__ == "__main__":
#     distance = 60
#     print(receiver_function(distance=distance))