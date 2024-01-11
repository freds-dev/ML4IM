import subprocess
import argparse

from utils.scene_helper import get_all_scenes

def start_scene_cross_validation(dataset_name):
    scenes = get_all_scenes()
    
    for scene in scenes:
        # Run the Bash script with arguments
        subprocess.run(['bash', "create_scene_split.sh", dataset_name, scene])
        
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start scenic cross validation.')
    parser.add_argument('-dataset', required=True, help='Name of the dataset which is used for training')

    args = parser.parse_args()
    start_scene_cross_validation(args.dataset)