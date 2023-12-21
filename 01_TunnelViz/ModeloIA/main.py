from ultralytics import YOLO
 
# Load the model.
model = YOLO('yolov8n.yaml')
 
# Training.
# results = model.train(
#    data='config.yaml',
#    imgsz=640,
#    epochs=50,
#    batch=8,
#    name='yolov8n_v8_50e'
# )

results = model.train(data="config.yaml", epochs=10, batch=16, name="planchuelas")