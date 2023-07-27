from ultralytics import YOLO
import os

# Load a model
weights = os.path.join('.', 'runs', 'detect', 'train13', 'weights', 'best.pt')
model = YOLO(weights)  # load a custom model

# Predict with the model
results = model('./Data/Images/images/00c133189dd16a45.jpg')  # predict on an image