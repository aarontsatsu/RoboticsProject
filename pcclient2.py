import time
import socket
import threading
import queue
import object_dist_finder as odf

# Set up client socket
server_ip = '192.168.137.222'
server_port = 27700
is_running = True
dist_found = False

timeout_seconds = 180
start_time = time.time()

# Shared queues for distance information
object_distance_queue = queue.Queue()
collection_distance_queue = queue.Queue()

# Flag to control camera feed processing
process_camera_feed = True

def get_object_distance():
    global process_camera_feed
    
    while is_running:
        if process_camera_feed:
            distance = odf.object_dist_finder()
            print('object distance', distance)
            object_distance_queue.put(distance)
        time.sleep(0.1)  

def get_collection_distance():
    global process_camera_feed
    
    while is_running:
        if process_camera_feed:
            distance = odf.collection_point_dist()
            print('collection distance', distance)
            collection_distance_queue.put(distance)
        time.sleep(0.1)  

# Start threads for reading distances
object_distance_thread = threading.Thread(target=get_object_distance)
collection_distance_thread = threading.Thread(target=get_collection_distance)

object_distance_thread.start()
collection_distance_thread.start()

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    while is_running and time.time() - start_time < timeout_seconds:

        try:
            # Retrieve the last known object distance from the thread
            object_distance = object_distance_queue.get(timeout=0.1)  
        except queue.Empty:
            object_distance = None

      

        if object_distance is None and dist_found is False:
            # Send the spin message for object distance
            data = 'spin,10,15,left'
            data_to_send = data
            client_socket.send(data_to_send.encode('utf-8'))

            # Receive a response from the server (optional)
            response = client_socket.recv(1024)
            print(f"Server response: {response.decode('utf-8')}")

        elif object_distance is not None:
            # Send the object distance to the server
            data_to_send = f'dist,{object_distance} '
            client_socket.send(data_to_send.encode('utf-8'))

            # check if object was picked
            response = client_socket.recv(1024)
            print(f"Server response: {response.decode('utf-8')}")
            dist_found = True

            obj_picked = bool(response.lower() == 'true')

            if obj_picked:
                dist_found = False
                try:
            # Retrieve the last known collection distance from the thread
                    collection_distance = collection_distance_queue.get(timeout=0.1)  
                except queue.Empty:
                    collection_distance = None
               

                if collection_distance is None and dist_found is False:
                    # Send the spin message for collection distance
                    data = 'spin,10,15,right'
                    data_to_send = data
                    client_socket.send(data_to_send.encode('utf-8'))

                    # Receive a response from the server (optional)
                    response = client_socket.recv(1024)
                    print(f"Server response: {response.decode('utf-8')}")

                elif collection_distance is not None:
                    dist_found = True
                    # Send the collection distance to the server
                    data_to_send = f'dist,{collection_distance} '
                    client_socket.send(data_to_send.encode('utf-8'))

                    # check if object was picked
                    response = client_socket.recv(1024)
                    print(f"Server response: {response.decode('utf-8')}")

                    sent_to_collection = bool(response.lower() == 'true')

                    if sent_to_collection:
                        
                        start_time = time.time()

    client_socket.close()

except Exception as e:
    print(f"Error during connection: {e}")

finally:
    # Stop the distance threads when exiting
    is_running = False
    object_distance_thread.join()
    collection_distance_thread.join()
