import numpy as np
import cv2, time
import objectDetection as od


#Define object specific variables  
dist = 0
focal = 300
pixels = 30
width = 7.6


#find the distance from the camera
def get_dist(rectange_params,image):
    distances = []
    start_time = time.time()

    while time.time() - start_time < 5:  # Run for 10 seconds
        # Find no. of pixels covered
        pixels = rectange_params[1][0]

        # Calculate distance
        dist = (width * focal) / pixels
        distances.append(dist)

        time.sleep(0.1)

    # Calculate the average distance
    # avg_distance = sum(distances) / len(distances)

    #median of the distances
    median_distance = sorted(distances)[len(distances) // 2]
    
    #Write on the image
    image = cv2.putText(image, 'Distance from Camera in CM :', org, font,  
       1, color, 2, cv2.LINE_AA)

    image = cv2.putText(image, str(round(median_distance,2)), (110,50), font,  
       fontScale, color, 1, cv2.LINE_AA)

    return image

#Extract Frames 
cap = cv2.VideoCapture('http://172.20.10.7:4747/video?start=0')


#basic constants for opencv functs
kernel = np.ones((3,3),'uint8')
font = cv2.FONT_HERSHEY_SIMPLEX 
org = (0,20)  
fontScale = 0.6 
color = (0, 0, 255) 
thickness = 2


cv2.namedWindow('Object Dist Measure ',cv2.WINDOW_NORMAL)
cv2.resizeWindow('Object Dist Measure ', 700,600)


def generate_color_range(base_color, tolerance=20):
    base_color_np = np.array(base_color)
    tolerance_np = np.array([tolerance, tolerance, tolerance])

    lower_bound = np.maximum(0, base_color_np - tolerance_np)
    upper_bound = np.minimum(255, base_color_np + tolerance_np)

    return lower_bound, upper_bound

def get_mask(lower_arr, upper_arr):
        lower = np.array(lower_arr)
        upper  = np.array(upper_arr)
        mask = cv2.inRange(hsv_img, lower, upper)
        return mask

#loop to capture video frames
while True:
    ret, img = cap.read()

    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    # color_hsv =  od.capture_obj_color()
    color_hsv = [77, 30, 76]
    # color_hsv = [color_hsv.join(',')]
    lower_arr, upper_arr = generate_color_range(color_hsv)
    
    # #predefined mask for green colour detection
    # lower = np.array([37, 51, 24])
    # upper = np.array([83, 104, 131])
    # mask = cv2.inRange(hsv_img, lower, upper)
     
    # Define the lower and upper bounds for black color in HSV
    mask = get_mask(lower_arr, upper_arr)
    #Remove Extra garbage from image
    d_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel,iterations = 5)


    #find the histogram
    cont,hei = cv2.findContours(d_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cont = sorted(cont, key = cv2.contourArea, reverse = True)[:1]

    for cnt in cont:
        #check for contour area
        if (cv2.contourArea(cnt)>100 and cv2.contourArea(cnt)<306000):

            #Draw a rectange on the contour
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect) 
            box = np.int0(box)
            cv2.drawContours(img,[box], -1,(255,0,0),3)
            
            img = get_dist(rect,img)

    cv2.imshow('Object Dist Measure ',img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()