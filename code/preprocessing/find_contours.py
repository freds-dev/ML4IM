import cv2
import numpy as np

def validate_band_input(input_bands: int, output_bands: [bool]):
    if input_bands not in [-1, 0, 1, 2]:
        raise Exception(f"Input bands must be in [-1, 0, 1, 2] but is {input_bands}")

    if len(output_bands) != 3:
        raise Exception("Length of output_bands must be 3!")

def find_contours(video_path, output_path, input_bands=-1, output_bands=[True, True, True]):
    validate_band_input(input_bands, output_bands)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Create a VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' for H.264 codec
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=True)  # Set isColor=True

    frame_count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if input_bands == -1:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray_frame = frame[:, :, input_bands]

        contours, _ = cv2.findContours(image=gray_frame, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

        black_channel = np.zeros_like(gray_frame, dtype=np.uint8)
        cv2.drawContours(image=black_channel, contours=contours, contourIdx=-1, color=255, thickness=2, lineType=cv2.LINE_AA)

        bands = []
        for i in range(len(output_bands)):
            if output_bands[i]:
                bands.append(black_channel)
            else:
                bands.append(frame[:, :, i])

        # Write the frame with contours to the output video
        out.write(cv2.merge(bands))

        if frame_count % 100 == 0:
            print(f"Processed frame {frame_count} from {total_frames}")

        frame_count += 1

    cap.release()
    out.release()
