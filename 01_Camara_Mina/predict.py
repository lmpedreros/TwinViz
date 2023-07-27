import cv2
import numpy as np
import os

# Load YOLOv8 model and configuration file
# Replace 'path/to/yolov8/config' and 'path/to/yolov8/weights' with actual paths
config = os.path.join('.', 'config.yaml')
weights = os.path.join('.', 'runs', 'detect', 'train13', 'weights', 'last.pt')
net = cv2.dnn.readNet(config, weights)

# Define classes (COCONames format)
classes = ['nail']

def predict_image(image_path):
    # Load image
    image = cv2.imread(image_path)
    height, width = image.shape[:2]

    # Preprocess the image (resize, normalize, etc.)
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Run forward pass to get output layers
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    detections = net.forward(output_layers)

    # Process the detections
    for detection in detections:
        for obj in detection:
            scores = obj[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Threshold for confidence
            if confidence > 0.5:
                x_center = int(obj[0] * width)
                y_center = int(obj[1] * height)
                w = int(obj[2] * width)
                h = int(obj[3] * height)

                # Calculate bounding box coordinates
                x_min = int(x_center - w / 2)
                y_min = int(y_center - h / 2)
                x_max = x_min + w
                y_max = y_min + h

                # Draw bounding box and label
                cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                cv2.putText(image, classes[class_id], (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the result
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Replace 'path/to/image.jpg' with the path to the image you want to detect objects in
image_path = './Data/Images/images/ffb76be8c8cc92c9.jpg'
predict_image(image_path)