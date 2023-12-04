from alive_progress import alive_bar
import cv2
import numpy as np

def optical_flow_farneback(input_video_path, output_video_path):
    # Open the video file
    cap = cv2.VideoCapture(input_video_path)

    # Get the video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create VideoWriter object to save the output
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Variables for Farneback Optical Flow
    prev_frame = None

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    with alive_bar(total_frames, title='Processing Frames') as bar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # If this is not the first frame, calculate optical flow
            if prev_frame is not None:
                # Calculate optical flow using Farneback method
                flow = cv2.calcOpticalFlowFarneback(prev_frame, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

                # Create an empty black image for channel 3
                black_channel = np.zeros_like(flow[..., 0], dtype=np.uint8)

                # Normalize optical flow values for visualization
                flow_norm = cv2.normalize(flow, None, 0, 255, cv2.NORM_MINMAX)
                flow_norm = flow_norm.astype(np.uint8)

                # Combine the original frame and optical flow results
                result_frame = cv2.merge([frame[:, :, 0], flow_norm[..., 1], black_channel])

                # Write the result to the output video
                out.write(result_frame)
            else:
                # Write the first frame to the output video
                out.write(frame)

            # Save the current frame for the next iteration
            prev_frame = gray
            bar()
    # Release video capture and writer objects
    cap.release()
    out.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()
