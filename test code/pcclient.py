

import time
import socket
import threading
# from .. import object_dist_finder as odf

# Set up client socket
server_ip = '192.168.137.252'
server_port = 27700
is_running = True
# odf.color
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    while is_running:
        user_input_str = input("Enter true or false: ")
        user_input_bool = bool(user_input_str.lower() == 'true')
        is_taken = user_input_bool


        if not is_taken:
            data ='spin,10,15,left'
            data_to_send = data
            client_socket.send(data_to_send.encode('utf-8'))

            # Receive a response from the server (optional)
            response = client_socket.recv(1024)
            print(f"Server response: {response.decode('utf-8')}")


        else:
            data = input("enter command: ")
            if data == "q":
                is_running = False
            
            data_to_send = data
            client_socket.send(data_to_send.encode('utf-8'))

            # Receive a response from the server (optional)
            response = client_socket.recv(1024)
            print(f"Server response: {response.decode('utf-8')}")

    client_socket.close()

except Exception as e:
    print(f"Error during connection: {e}")

