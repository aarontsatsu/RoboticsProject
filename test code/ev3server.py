#!/usr/bin/env python3

import socket
import threading
from time import sleep
from gripper import open_gripper, close_gripper
from ev3movement import driveStraight, stop_motors, spin

bind_ip = "192.168.137.146"
bind_port = 27700
# create and bind a new socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)
print("Server is listening on %s:%d" % (bind_ip, bind_port))

server_running = True
is_connected = True
print("global1: ", is_connected)
command_lock = threading.Lock()
is_connected_lock = threading.Lock()
current_command = 'None'


def execute_command():
    global current_command
    print("global 2: ", is_connected)
    while is_connected:
        with command_lock:
            if current_command == 'stop':
                stop_motors()
            elif 'open' in current_command:
                open_gripper()
            elif 'close' in current_command:
                close_gripper()
            elif 'drive' in current_command:
                _, speed, direction = current_command.split(',')
                driveStraight(int(speed), int(direction))
                
            elif 'spin' in current_command:
                _, angle_deg, motor_speed, direction =  current_command.split(',')
                spin(int(angle_deg), int(motor_speed), direction)


def clientHandler(client_socket):
    global is_connected, current_command
    print("global3: ", is_connected)

    while True:
        with is_connected_lock:
            if not is_connected:
                break
        # send a message to the client
        client_socket.send("ready".encode())
        # receive and display a message from the client
        request = client_socket.recv(1024)
        print("Received \"" + request.decode() + "\" from client")
        decoded_data = request.decode('utf-8').strip()

        if decoded_data == 'q':
            client_socket.send("client closed".encode())
            is_connected = False
            print("global4: ", is_connected)

        else:
            with command_lock:
                current_command = decoded_data

    # Close the server socket when the program is terminated
    client_socket.close()
    print("Connection closed")


# Start the command executor thread
executor_thread = threading.Thread(target=execute_command)
executor_thread.start()

while server_running:
    with is_connected_lock:
        is_connected = True
    print("global5: ", is_connected)

    try:
        # wait for client to connect
        client, addr = server.accept()
        print("client: ",client)
        if client:
            is_connected = True

        print('global10: ', is_connected)

        print("Client connected " + str(addr))
        # create and start a thread to handle the client
        client_handler = threading.Thread(target=clientHandler, args=(client,))
        client_handler.start()
        print("global7: ", is_connected)


    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C) to gracefully stop the server
        print("Server terminated by user")
        is_connected = False
        server_running = False

    except Exception as e:
        print("Error accepting client connection:", str(e))

# Wait for the client handler thread to finish
client_handler.join()

# Wait for the command executor thread to finish
executor_thread.join()

# Close the server socket
server.close()
