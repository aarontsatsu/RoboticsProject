import cv2
import objectDetection as od
import dist_measure as dm

window_name = 'Object Dist Measure'

cap = cv2.VideoCapture('http://172.16.0.245:4747/video?start=0')
color = od.capture_obj_color(cap, window_name)
dm.capture_obj_dist(cap, window_name, color)

cap.release()
cv2.destroyAllWindows()

# if distance is less than a certain length we can quit 
# how to pass distance