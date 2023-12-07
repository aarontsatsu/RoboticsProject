import time
import socket
import threading
import object_dist_finder as odf

# Set up client socket
server_ip = '192.168.137.222'
server_port = 27700
is_running = True

timeout_seconds = 180
start_time = time.time()

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    while is_running and time.time() - start_time < timeout_seconds:
        
        # look for object 
        distance = odf.object_dist_finder()
        if distance != 0 :
            data_to_send = f'dist:,{distance} '
            client_socket.send(data_to_send.encode('utf-8'))

            # check if object was picked
            response = client_socket.recv(1024)
            print(f"Server response: {response.decode('utf-8')}")

            obj_picked = bool(response.lower() == 'true')

            if obj_picked:
                distance = odf.collection_point_dist()

                if distance != 0 :
                    data_to_send = f'dist:,{distance} '
                    client_socket.send(data_to_send.encode('utf-8'))

                    # check if object was picked
                    response = client_socket.recv(1024)
                    print(f"Server response: {response.decode('utf-8')}")
                    sent_to_collection = bool(response.lower() == 'true')
                    if sent_to_collection:
                        start_time = time.time()

        # If no distance is received, you may want to break or handle it accordingly

        else:
            print("No distance received. Exiting loop.")
            break

    client_socket.close()

except Exception as e:
    print(f"Error during connection: {e}")

