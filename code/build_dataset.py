import os
import argparse

from utils.file_system import create_directory
from utils.helper import  percentage_floored, pick_n_random_items, read_ndjson
from utils.labelbox_to_coco import video_is_labeled, write_data_row

from utils.paths import get_annotations_path, get_video_dir, get_dataset_dir
import cv2
from pathlib import Path

def build_dataset(video_dir_name: str, dataset_dir_name: str, amount_videos: int, frames_per_video: int):
    """
    Args:
        video_dir_name (str): Path to the directory containing video files.
            Constraints: Must be a valid path. Raises FileNotFoundError if the specified directory does not exist.

        dataset_dir_name (str): Path for the output dataset directory.
            Constraints: Must be a valid path for the output dataset directory. It should not already exist.
            Raises an Exception if the dataset directory already exists.

        amount_videos (int): Number of videos to include in the dataset.
            Constraints: Must be a positive integer.
            Raises an Exception if the requested number of videos is greater than the actual number of labeled videos.

        frames_per_video (int): Number of frames to include per video.
            Constraints: Must be a positive integer.

    Returns:
        None

    Raises:
        FileNotFoundError: If the specified video directory does not exist.
        Exception: If the dataset directory already exists or if the requested number of videos is greater than the actual number of labeled videos.

    """    
    dataset_dir = get_dataset_dir(dataset_dir_name)
    if os.path.exists(dataset_dir):
        raise Exception(f"The dataset directory \"{dataset_dir}\" is already existent and therefore not useable. HINT: Choose another dataset_dir_name")
    
    video_dir =  get_video_dir(video_dir_name)
    anotation_location = get_annotations_path()
    
    data = read_ndjson(anotation_location)
    data = [d for d in data if video_is_labeled(d)]
    print(f"{len(data)} videos are labeled")
    if len(data) < amount_videos:
        raise Exception(f"Requested amount of videos ({amount_videos}) is greater than actual labeled videos ({len(data)}). HINT: Decrease amount_videos")
    
    amount_validation_videos = percentage_floored(amount_videos, 0.1)
    amount_test_videos = percentage_floored(amount_videos, 0.1)

    testing_data, data = pick_n_random_items(data,amount_test_videos)
    validation_data, data = pick_n_random_items(data,amount_validation_videos)
    data, _ = pick_n_random_items(data, amount_videos - (amount_validation_videos + amount_test_videos))
     
    # Create directory structure
    create_directory(dataset_dir)
    create_directory(os.path.join(dataset_dir, "train"))
    create_directory(os.path.join(dataset_dir, "val"))
    create_directory(os.path.join(dataset_dir, "test"))
    
    # Copy input into data.yaml
    write_dataset_yaml(dataset_dir)
        
    for dir in ["train","val","test"]:
        create_directory(os.path.join(dataset_dir,dir,"images"))
        create_directory(os.path.join(dataset_dir,dir,"labels"))
    
    for i in range(len(data)):
        write_data_row(data[i],(i+1),dataset_dir,video_dir, frames_per_video, "train")

    for i in range(len(validation_data)):
        write_data_row(validation_data[i],(i+1),dataset_dir,video_dir, frames_per_video, "val")

    for i in range(len(testing_data)):
        write_data_row(testing_data[i],(i+1),dataset_dir,video_dir, frames_per_video, "test")

def write_dataset_yaml(dataset_dir):
    with open(os.path.join(dataset_dir,"data.yaml"),"w") as f:
        f.write(
            """
train: ./train/images 
val: ./val/images
test: ./test/images
nc: 1 
names: ['insect']
            """
        )
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process videos.')
    parser.add_argument('-video_dir_name', required=True, help='Path to the source videos folder')
    parser.add_argument('-dataset_name', required=True, help='Name of the created dataset')
    parser.add_argument('-amount_videos', required=True, help='Amount of random choosen videos for the dataset')
    parser.add_argument('-frames_per_video', required=True, help='Amount of frames per video')

    args = parser.parse_args()
   
    video_dir_name = args.video_dir_name
    dataset_name = args.dataset_name
    amount_videos = int(args.amount_videos)
    frames_per_video = int(args.frames_per_video)
    
    build_dataset(video_dir_name,dataset_name,amount_videos,frames_per_video)
 