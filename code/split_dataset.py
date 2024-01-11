import math
import multiprocessing
import os
import argparse
import threading

from utils.file_system import create_directory
from utils.helper import  percentage_floored, pick_n_random_items, read_ndjson,chunks,pop_multiple_items
from utils.labelbox_to_coco import get_video_location, video_is_labeled, write_data_row
from utils.scene_helper import get_scene_to_video_combination
from utils.paths import get_annotations_path, get_video_dir, get_dataset_dir

def build_dataset_worker(video_dir, dataset_dir, data, frames_per_video, subset,chunk_size, chunk_id):
    for i in range(len(data)):
        write_data_row(data[i],(chunk_size * chunk_id)+i +1  , dataset_dir, video_dir, frames_per_video, subset)

def split_dataset(video_dir_name: str, dataset_dir_name: str, amount_videos: int, frames_per_video: int, scene = "",core_capacity_factor = 0.25):
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
    assert(core_capacity_factor > 0 and core_capacity_factor < 1)
    if amount_videos < 1:
        amount_videos = 10000
        
    if frames_per_video <1:
        frames_per_video = 100000000000
    dataset_dir = get_dataset_dir(dataset_dir_name)
    if os.path.exists(dataset_dir):
        raise Exception(f"The dataset directory \"{dataset_dir}\" is already existent and therefore not useable. HINT: Choose another dataset_dir_name")
    
    video_dir =  get_video_dir(video_dir_name)
    anotation_location = get_annotations_path()
    
    data = read_ndjson(anotation_location)
    data = [d for d in data if video_is_labeled(d)]
    data = [d for d in data if os.path.exists(get_video_location(video_dir,d))]
    if(amount_videos > len(data)):
        amount_videos = len(data)
        print(f"INFO: Reset amount videos to {len(data)}, because that is the amount of available videos")
    
    
    print(f"{len(data)} videos are labeled")
    
    scenes = get_scene_to_video_combination()
    ids = scenes[scene]
    validation_data = pop_multiple_items(data,ids)
    # Create directory structure
    create_directory(dataset_dir)
    create_directory(os.path.join(dataset_dir, "train"))
    create_directory(os.path.join(dataset_dir, "val"))
    
    # Copy input into data.yaml
    write_dataset_yaml(dataset_dir)
        
    for dir in ["train","val"]:
        create_directory(os.path.join(dataset_dir,dir,"images"))
        create_directory(os.path.join(dataset_dir,dir,"labels"))
    
       # Split data for multithreading
    data_threads, validation_threads = [], []
    
    
    # Minus two for reserving two cores for saving validation and test data
    num_cores = math.floor(multiprocessing.cpu_count() * core_capacity_factor) - 1
    print(f"{num_cores} cores are available")
    # Multithreading for training data
    data_chunks = list(chunks(data, max(len(data) // num_cores, 1)))
    for i in range(len(data_chunks)):
        thread = threading.Thread(
                target=build_dataset_worker,
                args=(video_dir, dataset_dir, data_chunks[i], frames_per_video, "train",max(len(data) // num_cores, 1),i)
            )
        data_threads.append(thread)
        thread.start()

        # Wait for all threads to finish
    # Non-threaded validation and testing data processing
    validation_threads.append(threading.Thread(
        target=build_dataset_worker,
        args=(video_dir, dataset_dir, validation_data, frames_per_video, "val",len(validation_data), 0)
    ))
    validation_threads[0].start()

    for thread in data_threads + validation_threads:
        thread.join()

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
    parser.add_argument('-amount_videos', default=0, help='Amount of random choosen videos for the dataset. If the value is below 1, all videos are taken (default = 0)')
    parser.add_argument('-frames_per_video', default=0, help='Amount of frames per video. If the value is below 1, all videos are taken (default = 0)')
    parser.add_argument('-scene', type=str,default="", help="name of scene for validation")
    parser.add_argument('-core_factor',default=0.25,help="Capacity of system and cores. The function will evaluate the number of available cpu cores and multiplies them with this factor, to determine the number of used threads. Needs to be in range [0,1] (default = 0.25)")

    args = parser.parse_args()
   
    video_dir_name = args.video_dir_name
    dataset_name = args.dataset_name
    amount_videos = int(args.amount_videos)
    frames_per_video = int(args.frames_per_video)
    core_factor = float(args.core_factor)
    scene = int(args.scene)
    
    
    split_dataset(video_dir_name,dataset_name,amount_videos,frames_per_video,scene,core_factor)
 