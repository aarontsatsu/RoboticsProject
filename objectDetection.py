import numpy as np
import cv2
import time

MIN_CONFIDENCE = 0.8

# found_object = False

def extract_dominant_color(image, bounding_box):
    # Extract the region of interest based on the bounding box
    (startX, startY, endX, endY) = bounding_box
    roi = image[startY:endY, startX:endX]
   
    # Reshape the ROI to a list of pixels
    pixels = roi.reshape((-1, 3))

    # Calculate the dominant color using k-means clustering. check chat gpt for the most cluster count
    k = 3  # Number of clusters (dominant color)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1)
    _, labels, centers = cv2.kmeans(pixels.astype(np.float32), k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    counts = np.bincount(labels.flatten())

    # Find the index of the most populated cluster
    most_populated_cluster_index = np.argmax(counts)

    # Get the color of the most populated cluster
    most_populated_color = centers[most_populated_cluster_index].astype(np.uint8)

    return most_populated_color

# image and tuple for  roi
def getHSV(image, roi):
    # Extract the dominant color in BGR
    dominant_color_bgr = extract_dominant_color(image, roi)

    # Replace this with your BGR value
    bgr_value = np.array([dominant_color_bgr], dtype=np.uint8)

    # Reshape to a 2D array
    bgr_value_2d = bgr_value.reshape(1, 1, 3)

    # Convert BGR to HSV
    hsv_value = cv2.cvtColor(bgr_value_2d, cv2.COLOR_BGR2HSV)[0][0]

    return hsv_value


def capture_obj_color(cap, window_name):
    # prototxt, and model paths
    prototxt_path = 'models\MobileNetSSD_deploy.prototxt'
    model_path = 'models\MobileNetSSD_deploy.caffemodel'

    classes = ["background", "aeroplane", "bicycle", "bird", "boat",
                "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                "sofa", "train", "tvmonitor"]

    np.random.seed(543210)
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # start model
    net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

    is_taken = False

    while not is_taken:
        ret,img = cap.read()

        height, width = img.shape[0], img.shape[1]
        # resize image 
        blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 0.007843, (300, 300), 127.5)

        net.setInput(blob)
        detected_objects = net.forward()
        # is_taken = False

        for i in range(detected_objects.shape[2]):
            confidence = detected_objects[0, 0, i, 2]
            if confidence > MIN_CONFIDENCE:
                class_index = int(detected_objects[0, 0, i, 1])
                # create bounding box
                upper_left_x = int(detected_objects[0, 0, i, 3] * width)
                lower_right_x = int(detected_objects[0, 0, i, 5] * width)
                low_right_y = int(detected_objects[0, 0, i, 6] * height)
                upper_left_y = int(detected_objects[0, 0, i, 4] * height)
                
                prediction_text = f'{classes[class_index]}: {confidence}'
                cv2.rectangle(img, (upper_left_x, upper_left_y), (lower_right_x, low_right_y), colors[class_index], 3)
                cv2.putText(img, prediction_text, (upper_left_x, 
                        upper_left_y-15 if upper_left_y > 30 else upper_left_y+15), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[class_index], 2)
                
                if classes[class_index] == "bottle" and not is_taken:
                    # Get the bounding box coordinates
                    box = detected_objects[0, 0, i, 3:7] * np.array([width, height, width, height])
                    (startX, startY, endX, endY) = box.astype("int")

                    # Extract the object from the image
                    object_image = img[startY:endY, startX:endX]

                    # Save the object image
                    cv2.imwrite(f"object_{classes[class_index]}.jpg", object_image)

                    dominant_color_bgr = getHSV(img, (startX, startY, endX, endY))

                    is_taken = True
                    return dominant_color_bgr
                
        cv2.imshow(window_name, img)
        cv2.waitKey(5)
    