import cv2
import objectDetection as od
import dist_measure as dm

def object_dist_finder():
    window_name = 'Object Dist Measure'

    cap = cv2.VideoCapture('http://192.168.137.198:4747/video?start=0')
    #cap = cv2.VideoCapture(0)

    color = od.capture_obj_color(cap, window_name)
    dist = dm.capture_obj_dist(cap, window_name, color)
    dist = round(dist, 2)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  
        cap.release()
        cv2.destroyAllWindows()
        exit()  

    cap.release()
    cv2.destroyAllWindows()

    return dist

def collection_point_dist():
    window_name = 'Collection Point Dist Measure'

    cap = cv2.VideoCapture('http://192.168.137.198:4747/video?start=0')
    #cap = cv2.VideoCapture(0)
    if cap.read()[0] == False:
        print("Not open")
    else: print("Open")

    color = [0,0,0]
    dist = dm.capture_obj_dist(cap, window_name, color)
    dist = round(dist, 2)

    key = cv2.waitKey(1) & 0xFF
    if key == 27: 
        cap.release()
        cv2.destroyAllWindows()
        exit()  

    cap.release()
    cv2.destroyAllWindows()

    return dist 
    
# print("obj", object_dist_finder())
# print("dist", collection_point_dist())