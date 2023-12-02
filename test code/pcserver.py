#!/usr/bin/env python3

import socket
import threading
from ev3dev2.motor import MoveTank, OUTPUT_C, OUTPUT_B


bind_ip = "192.168.137.146" 
bind_port = 27700 
# create and bind a new socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)
print("Server is listening on %s:%d" % (bind_ip, bind_port))

server_running = True

# initailize motors
tank = MoveTank(OUTPUT_B, OUTPUT_C)

# global vars
WHEEL_CIRCUMFRENCE = 19.5
BASELINE = 14.6 

# Distance is in centimeters
# Motor speed is between -1000 and 1000
def driveStraight(speed, distance):
    '''function takes in two params, distance and speed and causes the bot to drive
      either forward or backward in in straight line for a given distance at a certain speed'''
    # Distance
    rotations_per_cent = 1/WHEEL_CIRCUMFRENCE
    rotation = distance * rotations_per_cent
    # Motor Speed
    motor_speed = (speed/1000)*100
    
    if not ( -1000<= speed and speed <= 1000):
        return -1
    
    tank.on_for_rotations(motor_speed, motor_speed, rotation)


def clientHandler(client_socket):
    # send a message to the client
    client_socket.send("ready".encode())
    # receive and display a message from the client
    request = client_socket.recv(1024)
    print("Received \"" + request.decode() + "\" from client")
    decoded_data = request.decode('utf-8').strip().split(',')

   
    if len(decoded_data) == 2:
        speed, direction = int(decoded_data[0]), int(decoded_data[1])
        driveStraight(speed, direction)
        gp.close_gripper()
    # close the connection again
    client_socket.close()
    print("Connection closed")

while server_running:
    try:
        # wait for client to connect
        client, addr = server.accept()
        print("Client connected " + str(addr))
        # create and start a thread to handle the client
        client_handler = threading.Thread(target=clientHandler, args=(client,))
        client_handler.start()

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C) to gracefully stop the server
        print("Server terminated by user")
        server_running = False
    except Exception as e:
        print("Error accepting client connection:", str(e))

# Close the server socket when the program is terminated
server.close()