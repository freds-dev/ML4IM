import cv2
import os

def bg_subtraction(video_path, output_path):
    print("Performing background subtraction...")
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
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=True)  # Set isColor=True

    # Create a background subtractor
    bg_subtractor = cv2.createBackgroundSubtractorMOG2()

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Apply background subtraction
        fg_mask = bg_subtractor.apply(frame)

        # Convert single-channel image to three-channel
        fg_mask_colored = cv2.cvtColor(fg_mask, cv2.COLOR_GRAY2BGR)

        # Write the frame with the foreground mask to the output video
        out.write(fg_mask_colored)

        # Print the progress
        frame_count += 1
        print(f"Processing Frame {frame_count}/{total_frames}")

    print("Background subtraction complete.")

    cap.release()
    out.release()
