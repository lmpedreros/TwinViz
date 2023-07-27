import os

# Function to convert Open Image Dataset format to YOLO format
def convert_to_yolo(open_image_file, yolo_file):
    with open(open_image_file, 'r') as open_image:
        with open(yolo_file, 'w') as yolo:
            for line in open_image:
                data = line.strip().split(' ')
                # Assuming Open Image Dataset format is [class_id, xmin, ymin, xmax, ymax]
                class_id = int(data[0])
                xmin, ymin, xmax, ymax = map(float, data[1:])
                x_center = (xmin + xmax) / 2
                y_center = (ymin + ymax) / 2
                width = xmax - xmin
                height = ymax - ymin
                # Assuming YOLO format is [class_id, x_center, y_center, width, height]
                yolo.write(f"{class_id} {x_center/1000} {y_center/1000} {width/1000} {height/1000}\n")

# Path to the directory containing Open Image Dataset annotation files
open_image_dir = 'Data/Labels/labels'
# Path to the directory where YOLO annotation files will be saved
yolo_dir = 'Data/labels/yolo'

# Create the YOLO annotation directory if it doesn't exist
os.makedirs(yolo_dir, exist_ok=True)

# Iterate through each annotation file in the Open Image Dataset directory
for file_name in os.listdir(open_image_dir):
    if file_name.endswith('.txt'):
        open_image_file = os.path.join(open_image_dir, file_name)
        yolo_file = os.path.join(yolo_dir, file_name)
        convert_to_yolo(open_image_file, yolo_file)

print("Conversion completed.")