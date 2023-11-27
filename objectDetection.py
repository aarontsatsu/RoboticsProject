import numpy as np
import cv2


# i want to classify objects as recyclable or not recyclable

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

cap = cv2.VideoCapture('')

while True:
    ret,image = cap.read()

    height, width = image.shape[0], image.shape[1]
    # resize image 
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

    net.setInput(blob)
    detected_objects = net.forward()

    for i in range(detected_objects.shape[2]):
        confidence = detected_objects[0, 0, i, 2]
        if confidence > min_confidence:
            class_index = int(detected_objects[0, 0, i, 1])
            upper_left_x = int(detected_objects[0, 0, i, 3] * width)
            lower_right_x = int(detected_objects[0, 0, i, 5] * width)
            low_right_y = int(detected_objects[0, 0, i, 6] * height)
            upper_left_y = int(detected_objects[0, 0, i, 4] * height)

            prediction_text = f'{classes[class_index]}: {confidence}'
            cv2.rectangle(image, (upper_left_x, upper_left_y), (lower_right_x, low_right_y), colors[class_index], 3)
            cv2.putText(image, prediction_text, (upper_left_x, 
                        upper_left_y-15 if upper_left_y > 30 else upper_left_y+15), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[class_index], 2)
            
    cv2.imshow('image', image)
    cv2.waitKey(5)
    
    
cv2.destroyAllWindows()
cap.release()