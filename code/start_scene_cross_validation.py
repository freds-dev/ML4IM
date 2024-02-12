import subprocess
import argparse

from utils.scene_helper import get_all_scenes

def start_scene_cross_validation(dataset_name,video_event_name,video_rgb_name,config_name):
    scenes = get_all_scenes()
    
    for scene in scenes:
        # Run the Bash script with arguments
        subprocess.run(['bash', "create_scene_split.sh", dataset_name, scene,video_event_name,video_rgb_name,config_name])
        
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start scenic cross validation.')
    parser.add_argument('-dataset', required=True, help='Name of the dataset which is used for training') 
    parser.add_argument("-video_event_name", type=str, required=True,help="Directory where the event videos are located")
    parser.add_argument("-video_rgb_name", type=str, required=True,help="Directory where the rgb videos are located")
    parser.add_argument("-config_name",type=str,required=True,help="Name of the configuration file")
   

    args = parser.parse_args()
    start_scene_cross_validation(args.dataset,args.video_event_name,args.video_rgb_name,args.config_name)