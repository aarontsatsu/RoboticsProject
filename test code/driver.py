from  ev3movement import driveStraight, spin, turn
import subprocess as sp

while True:
    spin(200, 30, 'left')
    spin(200, 30, 'right')
    spin(200, 30, 'left')

    