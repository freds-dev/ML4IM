from alive_progress import alive_bar
import cv2
import numpy as np


def morph(video_path, output_path, kernel_size=5):
    print("Performing morphological operations...")
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

    # Define a kernel for morphological operations
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    with alive_bar(total_frames, title='Processing Frames') as bar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Apply threshold to create a binary image
            _, binary_mask = cv2.threshold(gray_frame, 1, 255, cv2.THRESH_BINARY)

            # Apply dilation followed by erosion
            morphed_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel)

            # Convert single-channel image to three-channel
            morphed_mask_colored = cv2.cvtColor(morphed_mask, cv2.COLOR_GRAY2BGR)

            # Write the frame with morphological operations to the output video
            out.write(morphed_mask_colored)

            bar()
    print("Morphological operations complete.")

    cap.release()
    out.release()
