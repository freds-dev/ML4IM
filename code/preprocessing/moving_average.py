import cv2
import numpy as np

def moving_average(video_path, output_path):
    c = cv2.VideoCapture(video_path)
    _, f = c.read()

    # Initialize the accumulators for moving averages
    avg1 = np.float32(np.abs(f - 127))
    avg2 = np.float32(np.abs(f - 127))

    fps = c.get(cv2.CAP_PROP_FPS)
    frame_width = int(c.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(c.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    frame_count = 0
    while True:
        _, f = c.read()

        if not _:
            break  # Break the loop if there are no more frames

        # Calculate the absolute difference from 127
        diff = np.abs(f - 127)

        # Accumulate weighted averages
        cv2.accumulateWeighted(diff, avg1, 0.1)
        cv2.accumulateWeighted(diff, avg2, 0.01)

        # Scale the accumulated averages
        res1 = cv2.convertScaleAbs(avg1)
        res2 = cv2.convertScaleAbs(avg2)

        # Assign the modified channel values to the second and third channels
        f[:, :, 1] = res1[:, :, 0]
        f[:, :, 2] = res2[:, :, 0]

        out.write(f)  # Write the modified frame to the output video file

        if frame_count % 20 == 0:
            print(frame_count)
        frame_count+=1
    # Release video capture and writer objects
    c.release()
    out.release()

    cv2.destroyAllWindows()