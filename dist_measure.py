import numpy as np
import cv2, time
import time


#Define object specific variables  
# dist = 0
FOCAL = 300
# pixels = 30
WIDTH = 7.6
#basic constants for opencv functs
KERNEL = np.ones((3,3),'uint8')
FONT = cv2.FONT_HERSHEY_SIMPLEX 
ORG = (0,20)  
FONTSCALE = 0.6 
COLOR = (0, 0, 255) 
THICKNESS = 2


#find the distance from the camera
def get_dist(rectange_params,image):
    distances = []
    start_time = time.time()

    while time.time() - start_time < 10:  # Run for 10 seconds
        # Find no. of pixels covered
        pixels = rectange_params[1][0]

    # Calculate distance
    dist = (WIDTH * FOCAL) / pixels
    # distances.append(dist)

        # time.sleep(0.1)

    # Calculate the average distance
    avg_distance = sum(distances) / len(distances)
    
    #Write on the image
    image = cv2.putText(image, 'Distance from Camera in CM :', ORG, FONT,  
       1, COLOR, 2, cv2.LINE_AA)

    image = cv2.putText(image, str(round(avg_distance,2)), (110,50), font,  
       fontScale, color, 1, cv2.LINE_AA)

    return image


def generate_color_range(base_color, tolerance=20):
    base_color_np = np.array(base_color)
    tolerance_np = np.array([tolerance, tolerance, tolerance])

    lower_bound = np.maximum(0, base_color_np - tolerance_np)
    upper_bound = np.minimum(255, base_color_np + tolerance_np)

    return lower_bound, upper_bound

def get_mask(lower_arr, upper_arr, hsv_img):
        lower = np.array(lower_arr)
        upper  = np.array(upper_arr)
        mask = cv2.inRange(hsv_img, lower, upper)
        return mask


def capture_obj_dist(cap, window_name, hsv):
    #loop to capture video frames
    while True:
        ret, img = cap.read()
        
        hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

        color_hsv = [hsv[0], hsv[1], hsv[2]]

        lower_arr, upper_arr = generate_color_range(color_hsv)

        # Define the lower and upper bounds for black color in HSV
        mask = get_mask(lower_arr, upper_arr, hsv_img)
        #Remove Extra garbage from image
        d_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL,iterations = 5)

        #find the histogram
        cont,hei = cv2.findContours(d_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cont = sorted(cont, key = cv2.contourArea, reverse = True)[:1]

        for cnt in cont:
            #check for contour area
            if (cv2.contourArea(cnt)>100 and cv2.contourArea(cnt)<306000):

                #Draw a rectange on the contour
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect) 
                box = np.intp(box)
                cv2.drawContours(img,[box], -1,(255,0,0),3)
                
                img = get_dist(rect,img)

        cv2.imshow(window_name,img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break