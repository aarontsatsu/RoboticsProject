import cv2
import objectDetection as od
import dist_measure as dm

def object_dist_finder():
    window_name = 'Object Dist Measure'

    cap = cv2.VideoCapture(0)
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

    cap = cv2.VideoCapture(0)
    color = [0, 100, 100]
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
    