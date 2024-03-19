import cv2
import os

def extract_frames(video_path, output_dir, start_frame, end_frame):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Set the starting frame position
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame - 1)

    # Get video properties
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Validate start_frame and end_frame values
    start_frame = max(1, min(start_frame, frame_count))
    end_frame = min(frame_count, max(end_frame, 1))

    # Loop through frames and save to the output directory
    for frame_number in range(start_frame, end_frame + 1):
        success, frame = cap.read()

        if not success:
            break  # Break the loop if no more frames are available

        # Create file name and save the frame
        file_name = f"{frame_number:05d}.jpg"
        output_path = os.path.join(output_dir, file_name)
        cv2.imwrite(output_path, frame)

        print(f"Processed frame {frame_number}/{frame_count}")

    # Release the video capture object
    cap.release()

if __name__ == "__main__":
    # Example usage
    input_video = "../../data/videos/hsv/2023-09-30-perennial_garden_extssd/2023-09-30_15-28-40.449020447_combined_000_4000.mp4"
    output_directory = "../../data/frames/hsv"
    start_frame = 0
    end_frame = 4000  # Adjust as needed

    extract_frames(input_video, output_directory, start_frame, end_frame)
