import cv2
import numpy as np

# This function reads each frame, converts it to grayscale,
# applies temporal filtering (in this case, an exponential moving average),
# and writes the filtered frame to the output video.
# You can adjust the filter_size parameter to control the strength of the temporal filtering.
# Larger values of filter_size will result in smoother but slower responses to changes in the input video.


def temporal_filtering(video_path, output_path,input_bands = -1,  output_bands = [True, True, True], filter_size=5):
    print(f"input_bands = {input_bands}")
    print(f"output_bands = {output_bands}")
    
    if input_bands not in [-1,0,1,2]:
        raise Exception(f"Input bands must be in [-1,0,1,2] but is {input_bands}")


    
    if len(output_bands) != 3:
        raise Exception("Length of output_bands must be 3!")


    print("Performing temporal filtering...")
    print(f"Input video path: {video_path}")
    print(f"Output folder: {output_path}")
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Get video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create a VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' for H.264 codec
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    out = cv2.VideoWriter(output_path, fourcc, fps,
                          (width, height), isColor=True)  # Set isColor=True

    # Initialize an accumulator
    accumulator = np.zeros((height, width), dtype=np.float32)

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to grayscale
        if input_bands == -1:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray_frame = frame[:,:,input_bands]
        # Convert the frame to float32 for accumulation
        gray_frame_float32 = gray_frame.astype(np.float32)

        # Apply temporal filtering (exponential moving average)
        accumulator = (1.0 - 1.0 / filter_size) * accumulator + \
            1.0 / filter_size * gray_frame_float32

        # Convert the accumulator to uint8 for visualization
        filtered_frame = np.uint8(accumulator)

        # Convert the filtered frame to a 3-channel image for visualization

        
        bands = []
        for i in range(len(output_bands)):
            if output_bands[i]:
                bands.append(filtered_frame)
            else:
                bands.append(frame[:,:,i])
                
        # Write the frame with temporal filtering to the output video
        out.write(cv2.merge(bands))

        # Print the progress
        frame_count += 1
        print(f"Processing Frame {frame_count}/{total_frames}")

    print("Temporal filtering complete.")

    cap.release()
    out.release()
