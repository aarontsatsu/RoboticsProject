#!/usr/bin/env python3

import socket
import threading
from time import sleep
from gripper import open_gripper, close_gripper
from ev3movement import driveStraight, stop_motors, spin
from config_script import receiver_function

bind_ip = '192.168.137.28'
bind_port = 27700
# create and bind a new socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)
print("Server is listening on %s:%d" % (bind_ip, bind_port))

server_running = True
distance_found = False
is_connected = True



def clientHandler(client_socket):
    global distance_found, is_connected
    client_socket.send("ready".encode())
    while is_connected:
        # send a message to the client
        # receive and display a message from the client
        request = client_socket.recv(1024)
        print("Received \"" + request.decode() + "\" from client")
        decoded_data = request.decode('utf-8').strip().split(',')

        if decoded_data[0] == 'spin':
            spin(int(decoded_data[1]),int(decoded_data[2]), decoded_data[3])
            client_socket.send("false".encode())
            
        elif decoded_data[0] == 'dist':
            stop_motors()
            status = receiver_function('obj', float(decoded_data[1]))
            print("proccessing ...")
            print(status)
            client_socket.send(str(status).encode())
            print('reached here')


        elif  decoded_data[0]:
            stop_motors()
            status = receiver_function('coll',float(decoded_data[1]))
            print("proccessing ...")
            print(status)
            client_socket.send(str(status).encode())
            print('reached here')
        else:
            client_socket.close()
            print("Connection closed")
            is_connected = False
    client_socket.close()
    print("Connection closed")



while server_running:
    
    try:
        # wait for client to connect
        client, addr = server.accept()
        print("Client connected " + str(addr))
        is_connected = True
        # create and start a thread to handle the client
        # spin
        
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
