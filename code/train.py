from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n.pt')  # load a pretrained model (recommended for training)

results = model.train(data='/Users/fred/Desktop/uni/master/sp_ml4im/ML4IM/data/datasets/bg_subtraction_temporal_filtering_small/data.yaml', batch=8, epochs=3, imgsz=320, device='cpu')