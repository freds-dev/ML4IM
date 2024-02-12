import os
import cv2
import numpy as np

from utils.video_calibration import *
from utils.helper import adjust_string_length

# Kein Aenderung
def show_image(im):
    cv2.imshow('image',im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def create_directory(directory_path):
    # Check if the directory already exists
    if not os.path.exists(directory_path):
        # If not, create the directory
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully")
    else:
        print(f"Directory '{directory_path}' already exists")    

def save_frames_from_video(video_path_event,video_path_rgb,config,output_folder, number_frames, video_id):
    # Open the video file
    cap_event = cv2.VideoCapture(video_path_event)
    cap_rgb = cv2.VideoCapture(video_path_rgb)

    # Get video properties
    total_frames = min(int(cap_event.get(cv2.CAP_PROP_FRAME_COUNT)),int(cap_rgb.get(cv2.CAP_PROP_FRAME_COUNT)))

    # Determine the number of frames to save
    frames_to_save = min(number_frames, total_frames)

    #with alive_bar(frames_to_save, title=f'Save video: {video_path}') as bar:
    frame_count = 0
    for frame_number in range(frames_to_save):
            ret_event, frame_event = cap_event.read()
            ret_rgb, frame_rgb = cap_rgb.read()
            if not ret_event or not ret_rgb:
                break  # Break the loop if there are no more frames

            # Save the frame as an image
            frame_filename = f'img_{video_id}_{adjust_string_length( str(frame_number + 1),6,"0")}.png'
            
            frame_event = crop_image(frame_event)
            frame_rgb = crop_image_rgb(frame_rgb)
            
            frame_event = cv2.resize(frame_event, dsize=(1280, 720))

            frame_event,_ = undistort_img(frame_event)
            frame_rgb,_ = undistort_img(frame_rgb, False)
            cv2.imwrite("tmp_event.png",frame_event)
            cv2.imwrite("tmp_rgb.png",frame_rgb)
            frame_rgb = translate_img(frame_rgb,frame_event.shape[1],frame_event.shape[0])
            cv2.imwrite("tmp_mapped.png",frame_rgb)
            
            frame = config.build_frame(frame_event,frame_rgb) 
            cv2.imwrite(os.path.join(str(output_folder), frame_filename),frame)
            #bar()
            if frame_count % 100 == 0:
                print(f"Save frame {frame_count} from video {video_id}")
            frame_count += 1
        # Release the video capture object
    cap_event.release()
    cap_rgb.release()


def write_file(path,content):
    # If dir is not exisitng just create it:
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    f = open(path, "w")
    f.write(content)
    f.close()
    print(f"Saved content to {path}")
    

def get_homography_matrix(x=0,y=12):   
    calibration_file = get_homography()
    fs = cv2.FileStorage(calibration_file, cv2.FILE_STORAGE_READ)
    homography_matrix = fs.getNode('H').mat()
    homography_matrix = homography_matrix @ np.array([ [1, 0, x], [0, 1, y], [0, 0, 1] ], dtype=np.float32)
    fs.release()
    return homography_matrix

def crop_image(frame):
    return frame[:1080, :]

def crop_image_rgb(image_matrix, target_height = 1200):
    height, width, channels = image_matrix.shape
    start_row = max(height - target_height, 0)

    cropped_image_matrix = image_matrix[start_row:, :, :]

    return cropped_image_matrix

