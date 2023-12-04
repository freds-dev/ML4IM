from alive_progress import alive_bar
import cv2


def contrast_enhancement(video_path, output_path):
    print("Performing contrast enhancement...")
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

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    with alive_bar(total_frames, title='Processing Frames') as bar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Apply histogram equalization to enhance contrast
            enhanced_frame = cv2.equalizeHist(gray_frame)

            # Convert single-channel image to three-channel
            enhanced_frame_colored = cv2.cvtColor(
                enhanced_frame, cv2.COLOR_GRAY2BGR)

            # Write the frame with contrast enhancement to the output video
            out.write(enhanced_frame_colored)

            # Print the progress
            bar()
        print("Contrast enhancement complete.")

    cap.release()
    out.release()
