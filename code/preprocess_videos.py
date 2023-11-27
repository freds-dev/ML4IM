import os
import argparse
import importlib.util

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

def preprocess_videos(txt_file, preprocessing_function_module, output_directory):
    # Check if the input file exists
    if not os.path.exists(txt_file):
        print(f"Error: File not found - {txt_file}")
        return

    # Read the video paths from the input file
    with open(txt_file, 'r') as file:
        video_paths = file.read().splitlines()

    print(f"preprocessing_function_module: {preprocessing_function_module}")

    # Split the module and function name
    try:
        module_name, function_name = preprocessing_function_module.split('.')
    except ValueError as e:
        print(f"Error splitting module and function name: {e}")
        return

    print(f"module_name: {module_name}")
    print(f"function_name: {function_name}")

    # Import the specified preprocessing function module
    try:
        module = importlib.import_module(f"{module_name}.{function_name}")
    except ImportError as e:
        print(f"Error importing module: {e}")
        return

    # Perform the specified function on each video path
    for video_path in video_paths:
        getattr(module, function_name)(video_path, output_directory)



def main():
    parser = argparse.ArgumentParser(description='Process videos.')
    parser.add_argument('-source', required=True, help='Path to the source videos folder')
    parser.add_argument('-txt', required=True, help='Path to the input text file')
    parser.add_argument('-save', required=True, help='Path to the output directory for preprocessed videos')
    parser.add_argument('-func', required=True, help='Module and function name for the preprocessing function (e.g., module_name.function_name)')

    args = parser.parse_args()

    # Example usage
    videos_to_process = args.source
    txt_file = args.txt
    directory_to_save = args.save
    preprocessing_function_module = args.func

    mp4_files = find_mp4_files(videos_to_process)
    write_to_file(txt_file, mp4_files)

    preprocess_videos(txt_file, preprocessing_function_module, output_directory=directory_to_save)

if __name__ == "__main__":
    main()
    # example usage: python3 preprocess_videos.py -source "videos" -txt "mp4_files.txt" -save "preprocessed_videos" -func "preprocessing.bg_subtraction"