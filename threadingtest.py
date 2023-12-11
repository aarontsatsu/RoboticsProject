import time
import socket
import threading
import queue
import object_dist_finder as odf


# Set up client socket
server_ip = '192.168.137.28'
server_port = 27700
is_running = True
dist_found = False
col_dist_found = False
first_run = False
obj_picked = None

timeout_seconds = 180
start_time = time.time()

# Create a lock
lock = threading.Lock()


# Create a queue for communication between threads
object_distance_queue = queue.Queue()
collection_distance_queue  = queue.Queue()

# Global variable to store the distance
global_obj_distance = None
global_col_distance = None

def get_object_distance():
    global global_obj_distance  # Use the global variable

    print("getting the object distance....")
    with lock:
        distance = odf.object_dist_finder()
        print('object distance', distance)
        object_distance_queue.put(distance)

        # Set the global distance variable
        global_obj_distance = distance

        # Check if the desired condition for ending the thread is met
        if distance is not None:
            return


def get_collection_distance():
    global global_col_distance  # Use the global variable

    print("getting the collection distance....")
    with lock:
        distance = odf.collection_point_dist()
        print('collection distance: ', distance)
        collection_distance_queue.put(distance)
       

        # Check if the desired condition for ending the thread is met
        if distance is not None:
            return




# Create the thread
object_distance_thread = threading.Thread(target=get_object_distance)
collection_distance_thread = threading.Thread(target=get_collection_distance)

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    object_distance_thread.start()

except Exception as e:
    print(f"Error during connection: {e}")

while is_running and time.time() - start_time < timeout_seconds:

    try:
        # Retrieve the last known object distance from the thread
        object_distance = object_distance_queue.get(timeout=0.1)        
    except queue.Empty:
        object_distance = None
    
    # no distance found -> spin
    if object_distance is None :
        # Send the spin message for object distance
        data = 'spin,10,15,left'
        data_to_send = data
        client_socket.send(data_to_send.encode('utf-8'))

        # Receive a response from the server (optional)
        response = client_socket.recv(1024)
        print(f"Server response  obj spin: {response.decode('utf-8')}")

    # distance found -> execute commands
    if object_distance:
        # Send the object distance to the server
        data_to_send = f'dist,{object_distance} '
        client_socket.send(data_to_send.encode('utf-8'))
        object_distance_thread.join()
            # check if object was picked
        try:
            # Add a confirmation step
            confirmation = client_socket.recv(1024)
            print(f"Server confirmation: {confirmation.decode('utf-8')}")

            # Wait for the actual response
            response = client_socket.recv(1024)
            print(f"Server response obj dist: {response.decode('utf-8')}")  
            
            obj_picked = bool(response.decode('utf-8').lower() == 'true') 
            # dist_found = True
            # first_run = True
            
        except socket.timeout:
            print("Timeout occurred while waiting for the server response.")
        except Exception as e:
            print(f"Error during recv: {e}")

    
    
    dist_found = False
    if obj_picked:
        

        # print("any distance found", dist_found)
        collection_distance_thread.start()
        collection_distance = None
        
        while collection_distance is None:
            # Send the spin message for collection distance
            data = 'spin,10,15,left'
            data_to_send = data
            client_socket.send(data_to_send.encode('utf-8'))

            # Receive a response from the server (optional)
            response = client_socket.recv(1024)
            print(f"Server response col spin: {response.decode('utf-8')}")

            try:
            # Retrieve the last known collection distance from the thread
                collection_distance = collection_distance_queue.get(timeout=0.1)
                print("collection queue: ",collection_distance)
            except queue.Empty:
                collection_distance = None

        if collection_distance:
            # col_dist_found = True
            # Send the collection distance to the server
            data_to_send = f'coll,{collection_distance} '
            client_socket.send(data_to_send.encode('utf-8'))

            # check if object was picked
            response = client_socket.recv(1024)
            print(f"Server response coll dist: {response.decode('utf-8')}")

            sent_to_collection = bool(response.lower() == 'true')
            collection_distance_thread.join()

            print("sent to collection point:", sent_to_collection)
            if sent_to_collection:
                print("job nots finished time to look again.....")
                start_time = time.time()
                object_distance_queue.empty()
                collection_distance_queue.empty()
                obj_picked = False
                

client_socket.close()


print("Both threads have finished.")
