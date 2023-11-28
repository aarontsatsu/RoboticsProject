

import time
import socket

# Set up client socket
server_ip = '172.20.10.4'
server_port = 27700

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

 
# Send data to the server
    data_to_send = "200, 30"
    client_socket.send(data_to_send.encode('utf-8'))

    # Receive a response from the server (optional)
    response = client_socket.recv(1024)
    print(f"Server response: {response.decode('utf-8')}")

    

except Exception as e:
    print(f"Error during connection: {e}")

finally:
    # Close the client socket
    client_socket.close()