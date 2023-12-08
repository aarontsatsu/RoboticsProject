#!/usr/bin/env python3

import socket
import threading
from time import sleep
from gripper import open_gripper, close_gripper
from ev3movement import driveStraight, stop_motors, spin
from config_script import receiver_function

bind_ip = "192.168.137.222"
bind_port = 27700
# create and bind a new socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)
print("Server is listening on %s:%d" % (bind_ip, bind_port))

server_running = True


def clientHandler(client_socket):
  
    # send a message to the client
    client_socket.send("ready".encode())
    # start spinning
    spin(10,15,"left")

    # receive and display a message from the client
    request = client_socket.recv(1024)
    if request:
        # stop spinning
        stop_motors()
    print("Received \"" + request.decode() + "\" from client")
    decoded_data = request.decode('utf-8').strip().split(',')
    receiver_function(int(decoded_data[1]))



    
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
        is_connected = False
        server_running = False

    except Exception as e:
        print("Error accepting client connection:", str(e))

# Wait for the client handler thread to finish
client_handler.join()

# Close the server socket
server.close()
