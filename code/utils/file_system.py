import os
import pathlib
from alive_progress import alive_bar
import cv2

from utils.helper import adjust_string_length

def create_directory(directory_path):
    # Check if the directory already exists
    if not os.path.exists(directory_path):
        # If not, create the directory
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully")
    else:
        print(f"Directory '{directory_path}' already exists")    

def save_frames_from_video(video_path,output_folder, number_frames, video_id):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Determine the number of frames to save
    frames_to_save = min(number_frames, total_frames)

    #with alive_bar(frames_to_save, title=f'Save video: {video_path}') as bar:
    frame_count = 0
    for frame_number in range(frames_to_save):
            ret, frame = cap.read()
            if not ret:
                break  # Break the loop if there are no more frames

            # Save the frame as an image
            frame_filename = f'img_{video_id}_{adjust_string_length( str(frame_number + 1),6,"0")}.png'
            frame = crop_image(frame)
            cv2.imwrite(os.path.join(str(output_folder), frame_filename),frame)
            #bar()
            if frame_count % 100 == 0:
                print(f"Save frame {frame_count} from video {video_id}")
            frame_count += 1
        # Release the video capture object
    cap.release()


def crop_image(frame):
    return frame[:1080, :]