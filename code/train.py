import argparse
from ultralytics import YOLO
from utils.paths import get_data_yaml, get_result_dir

def train(dataset, epochs = 100, batch = -1, save_period = 10, name = "first_run", model_path='yolov8n.yaml', exist_ok = False,device=0, plots=True):
    model = YOLO('yolov8n.pt')
    yaml_file = get_data_yaml(dataset)
    
    results = model.train(
        model=model_path,
        data=yaml_file,
        epochs=epochs,
        patience=epochs,
        batch=batch,
        save=True,
        save_period=save_period,
        device=device,
        project=get_result_dir(dataset),
        name=name,
        exist_ok=False,
        pretrained=True,
        plots=plots
    )
    
    return results

def main():
    parser = argparse.ArgumentParser(description='Train YOLO model.')
    parser.add_argument('-dataset', required=True, help='Name of the dataset can be found as it is directory in your "data/datasets" directory.')
    parser.add_argument('-epochs', type=int, default=100, help='Number of training epochs (default: 100).')
    parser.add_argument('-batch', type=int, default=-1, help='Batch size for training, -1 uses an automatic approach to define a well defined batch size(default: -1).')
    parser.add_argument('-save_period', type=int, default=10, help='Save model checkpoints every N epochs (default: 10).')
    parser.add_argument('-name', default="first_run", help='The name of the run. It will use the dataset as project and this name as name of the actual running experiment')
    parser.add_argument('-model_path', default='yolov8n.yaml', help='Path to the YOLO model configuration file (default: yolov8n.yaml).')
    parser.add_argument('-device', default=0, help='Device index for training (default: 0). Use arrays (e.g. [0,1] for multiple gpu usage and "cpu" for using cpu)')
    parser.add_argument('-exist_ok', action='store_true', help='Allow overwriting the project directory if it already exists.')
    parser.add_argument('-plots', action='store_true', help='Generate plots for each epoch(default: True).')

    args = parser.parse_args()

    train(
        dataset=args.dataset,
        epochs=args.epochs,
        batch=args.batch,
        save_period=args.save_period,
        name=args.name,
        model_path=args.model_path,
        device=args.device,
        exist_ok=args.exist_ok,
        plots=args.plots
    )

if __name__ == "__main__":
    main()
