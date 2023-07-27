from ultralytics import YOLO
import os

# Load a model
model_path = os.path.join('.', 'runs', 'detect', 'train13', 'weights', 'last.pt')
model = YOLO(model_path)  # load a custom model

# Validate the model
metrics = model.val()  # no arguments needed, dataset and settings remembered
metrics.box.map    # map50-95
metrics.box.map50  # map50
metrics.box.map75  # map75
metrics.box.maps   # a list contains map50-95 of each category