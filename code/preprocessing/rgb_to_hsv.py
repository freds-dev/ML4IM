import cv2
from alive_progress import alive_bar 

def rgb_to_hsv(input_video_path, output_video_path):
    print(f"Process video: {input_video_path}")
    # Open the video file
    cap = cv2.VideoCapture(input_video_path)

    # Get the video properties
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = int(cap.get(5))
    

    # Create VideoWriter object to save the processed video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can change the codec as needed
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    with alive_bar(total_frames, title='Processing Frames') as bar:
        # Loop through each frame in the video
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert RGB to HSV
            frame_hsv = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2HSV)

            # Split the HSV image into individual channels
            h, s, v = cv2.split(frame_hsv)

            # Use the HSV channels to modify the RGB channels
            modified_frame = cv2.merge([h, s, v])

            # Convert RGB back to BGR for writing to the video file
            modified_frame_bgr = cv2.cvtColor(modified_frame, cv2.COLOR_RGB2BGR)

            # Write the modified frame to the output video
            out.write(modified_frame_bgr)

            # Display the progression
            bar()
        # Release video capture and writer objects
    cap.release()
    out.release()

    print("Processing complete. Video saved at:", output_video_path)
