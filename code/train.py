from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n.pt')  # load a pretrained model (recommended for training)

# Train the model with 2 GPUs
results = model.train(data='/Users/fred/Desktop/uni/master/sp_ml4im/ML4IM/data/datasets/bg_substraction/data.yaml', batch=8, epochs=3, imgsz=320, device='cpu')