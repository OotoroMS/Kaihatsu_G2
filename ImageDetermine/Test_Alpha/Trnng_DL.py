from ultralytics import YOLO

model = YOLO('yolov8n.yaml')  # または事前学習済みモデル 'yolov8n.pt'
results = model.train(data='ImageDetermine/Test_Alpha/data.yaml', epochs=50, imgsz=640)