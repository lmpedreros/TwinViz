# from ultralytics import YOLO
# import cv2

# # Load a model
# model = YOLO('bestBacan.pt')  # pretrained YOLOv8n model

# # Run batched inference on a list of images
# results = model(['predict/1000002231.jpg', 'predict/1000002232.jpg', 'predict/1000002233.jpg', 'predict/1000002234.jpg',
#                  'predict/1000002235.jpg', 'predict/1000002236.jpg', 'predict/1000002237.jpg', 'predict/1000002238.jpg',
#                  'predict/1000002239.jpg', 'predict/1000002240.jpg'])  # return a list of Results objects

# # Process results list
# img = cv2.imread('captura.jpg')
# for result in results:
#     boxes = result.boxes.cpu().numpy()
#     for i, box in enumerate(boxes):
#         r = box.xyxy[0].astype(int)
#         crop = img[r[1]:r[3], r[0]:r[2]]
#         cv2.imwrite(str(i) + ".jpg", crop)

from ultralytics import YOLO
import cv2
import numpy as np

# Load a model
model = YOLO('bestBacan.pt')  # pretrained YOLOv8n model

# List of image file paths
image_paths = [
    'predict/1000002231.jpg', 'predict/1000002232.jpg', 'predict/1000002233.jpg', 'predict/1000002234.jpg',
    'predict/1000002235.jpg', 'predict/1000002236.jpg', 'predict/1000002237.jpg', 'predict/1000002238.jpg',
    'predict/1000002239.jpg', 'predict/1000002240.jpg'
]

# Process images and save with predictions painted in red
for image_path in image_paths:
    img = cv2.imread(image_path)
    results = model(image_path)  # Perform inference on a single image

    # for box in results.xyxy[0]:
    #     label = int(box[5])
    #     conf = box[4]
    #     if conf > 0.5:  # You can adjust the confidence threshold as needed
    #         box = box.cpu().numpy().astype(int)
    #         img = cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 2)  # Draw a red bounding box
    #         img = cv2.putText(img, f"{label} ({conf:.2f})", (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)  # Label in red
    
    for result in results:                                         # iterate results
        boxes = result.boxes.cpu().numpy()    
        conf = boxes.conf
        print(f"{conf[0]} esta es la confidencia")
        for box in boxes:                                          # iterate boxes
            r = box.xyxy[0].astype(int)                            # get corner points as int
            label = result.names[int(box.cls[0])]                     # get boxes on cpu in numpy
            print(r)                                               # print boxes
            print(label)
            print(conf)
            img = cv2.rectangle(img, r[:2], r[2:], (0, 0, 255), 2)   # draw boxes on img
            #img = cv2.putText(img, f"{label} ({conf[0]:.2f})", (int(r[:2]), int(r[2:])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            img = cv2.putText(img, label.upper(), (int(r[:2]), int(r[2:] - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
            #image = cv2.putText(image, 'OpenCV', org, font, fontScale, color, thickness, cv2.LINE_AA) 


    # Save the modified image with bounding boxes and labels in red
    output_path = f"output_{image_path.split('/')[-1]}"  # Save the image with a new filename
    cv2.imwrite(output_path, img)