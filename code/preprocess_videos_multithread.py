import math
import multiprocessing
import os
import argparse
import importlib.util
import threading


from utils.helper import chunks
# Find all .mp4 files in the specified folder recursively


def find_mp4_files(folder_path):
    mp4_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".mp4"):
                mp4_files.append(os.path.join(root, file))
    return mp4_files

# Write the paths to the output file


def write_to_file(output_path, mp4_files):
    with open(output_path, 'w') as file:
        for mp4_file in mp4_files:
            file.write(mp4_file + '\n')


def preprocess_videos(txt_file, preprocessing_function_module, output_directory, source_directory, core_capacity_factor = 0.2):
    # Check if the input file exists
    if not os.path.exists(txt_file):
        print(f"Error: File not found - {txt_file}")
        return

    # Read the video paths from the input file
    with open(txt_file, 'r') as file:
        video_paths = file.read().splitlines()

    # Split the module and function name
    try:
        module_name, function_name = preprocessing_function_module.split('.')
    except ValueError as e:
        print(f"Error splitting module and function name: {e}")
        return

    # Import the specified preprocessing function module
    try:
        module = importlib.import_module(f"{module_name}.{function_name}")
    except ImportError as e:
        print(f"Error importing module: {e}")
        return


    def save_and_process(video_path,source_directory,output_directory):
        print("Save and process ...")
        current_source_directory = os.path.dirname(video_path)
        relative_source_directory = os.path.relpath(
                current_source_directory, source_directory)
        output_subdirectory = os.path.join(
                output_directory, relative_source_directory)
        os.makedirs(output_subdirectory, exist_ok=True)

            # Get the output video path within the subdirectory
        output_video_path = os.path.join(
                output_subdirectory, os.path.basename(video_path))

            # Perform the specified function on each video path
            
        getattr(module, function_name)(video_path, output_video_path)

    
    def tmp(xs,source_directory,output_directory):
        for x in xs:
            save_and_process(x,source_directory,output_directory)
    
    
    num_cores = math.floor(multiprocessing.cpu_count() * core_capacity_factor)
    print(f"{num_cores} cores are available")
    path_chunks = list(chunks(video_paths, max((len(video_paths) // num_cores + 1), 1)))
    threads = []
    for i in range(len(path_chunks)):
        thread = threading.Thread(
            target = tmp,
            args= (path_chunks[i],source_directory,output_directory)
        )
        print(f"Start thread on {path_chunks[i]}")
        threads.append(thread)
        thread.start()
        
    
    for thread in threads:
        thread.join()
    

def main():
    parser = argparse.ArgumentParser(description='Process videos.')
    parser.add_argument('-source', required=True,
                        help='Path to the source videos folder')
    parser.add_argument('-txt', required=True,
                        help='Path to the input text file')
    parser.add_argument('-save', required=True,
                        help='Path to the output directory for preprocessed videos')
    parser.add_argument('-func', required=True,
                        help='Module and function name for the preprocessing function (e.g., module_name.function_name)')
    parser.add_argument('-core_factor',default=0.25,help="Capacity of system and cores. The function will evaluate the number of available cpu cores and multiplies them with this factor, to determine the number of used threads. Needs to be in range [0,1] (default = 0.25)")
    
    args = parser.parse_args()

    # Example usage
    videos_to_process = args.source
    txt_file = args.txt
    directory_to_save = args.save
    preprocessing_function_module = args.func
    core_factor = args.core_factor
    
    mp4_files = find_mp4_files(videos_to_process)
    write_to_file(txt_file, mp4_files)

    preprocess_videos(txt_file, preprocessing_function_module,
                      output_directory=directory_to_save, source_directory=videos_to_process, core_capacity_factor=core_factor)


if __name__ == "__main__":
    main()
    # example usage: python3 preprocess_videos.py -source "videos" -txt "mp4_files.txt" -save "preprocessed_videos" -func "preprocessing.bg_subtraction"