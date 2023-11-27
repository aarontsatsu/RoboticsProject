import numpy as np
import cv2

def extract_dominant_color(image, bounding_box):
    # Extract the region of interest (ROI) based on the bounding box
    (startX, startY, endX, endY) = bounding_box
    roi = image[startY:endY, startX:endX]
   
    # Reshape the ROI to a list of pixels
    pixels = roi.reshape((-1, 3))

    # Calculate the dominant color using k-means clustering
    k = 1  # Number of clusters (dominant color)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1)
    _, labels, centers = cv2.kmeans(pixels.astype(np.float32), k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Get the dominant color
    dominant_color = centers[0].astype(np.uint8)

    return dominant_color

# prototxt, and model paths
prototxt_path = 'models\MobileNetSSD_deploy.prototxt'
model_path = 'models\MobileNetSSD_deploy.caffemodel'

min_confidence = 0.8 # play around with this and observe your results 

classes = ["background", "aeroplane", "bicycle", "bird", "boat",
              "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
              "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
              "sofa", "train", "tvmonitor"]

np.random.seed(543210)
colors = np.random.uniform(0, 255, size=(len(classes), 3))

net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

cap = cv2.VideoCapture('http://172.16.4.142:4747/video?start=0')

while True:
    ret,image = cap.read()

    height, width = image.shape[0], image.shape[1]
    # resize image 
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

    net.setInput(blob)
    detected_objects = net.forward()
    is_taken = False

    for i in range(detected_objects.shape[2]):
        confidence = detected_objects[0, 0, i, 2]
        if confidence > min_confidence:
           

            class_index = int(detected_objects[0, 0, i, 1])
            upper_left_x = int(detected_objects[0, 0, i, 3] * width)
            lower_right_x = int(detected_objects[0, 0, i, 5] * width)
            low_right_y = int(detected_objects[0, 0, i, 6] * height)
            upper_left_y = int(detected_objects[0, 0, i, 4] * height)
            
            if classes[class_index] == "bottle" and not is_taken:
                # Get the bounding box coordinates
                box = detected_objects[0, 0, i, 3:7] * np.array([width, height, width, height])
                (startX, startY, endX, endY) = box.astype("int")

                # Extract the object from the image
                object_image = image[startY:endY, startX:endX]

                # Save the object image
                cv2.imwrite(f"object_{i + 1}.jpg", object_image)
                
                # Extract the dominant color in BGR
                dominant_color_bgr = extract_dominant_color(image, (startX, startY, endX, endY))


                # Replace this with your BGR value
                bgr_value = np.array([dominant_color_bgr], dtype=np.uint8)

                # Reshape to a 2D array
                bgr_value_2d = bgr_value.reshape(1, 1, 3)

                # Convert BGR to HSV
                hsv_value = cv2.cvtColor(bgr_value_2d, cv2.COLOR_BGR2HSV)[0][0]
                # Convert BGR to HSV
                dominant_color_hsv = cv2.cvtColor(np.uint8([[dominant_color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]

                print(f"Dominant Color (BGR) for Object {i + 1}: {dominant_color_bgr}")
                print(f"Dominant Color (HSV) for Object {i + 1}: {hsv_value}") #returm the hsv value

                is_taken = True



            prediction_text = f'{classes[class_index]}: {confidence}'
            cv2.rectangle(image, (upper_left_x, upper_left_y), (lower_right_x, low_right_y), colors[class_index], 3)
            cv2.putText(image, prediction_text, (upper_left_x, 
                        upper_left_y-15 if upper_left_y > 30 else upper_left_y+15), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[class_index], 2)
            
    cv2.imshow('image', image)
    cv2.waitKey(5)
    
    
cv2.destroyAllWindows()
cap.release()