from alive_progress import alive_bar
import cv2

def bg_subtraction(video_path, output_path,input_bands = -1,  output_bands = [True, True, True]):
    print("Performing background subtraction...")
    print(f"Input video path: {video_path}")
    print(f"Output folder: {output_path}")
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    print(f"input_bands = {input_bands}")
    print(f"output_bands = {output_bands}")
    
    if input_bands not in [-1,0,1,2]:
        raise Exception(f"Input bands must be in [-1,0,1,2] but is {input_bands}")


    
    if len(output_bands) != 3:
        raise Exception("Length of output_bands must be 3!")

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
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    with alive_bar(total_frames, title='Processing Frames') as bar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if input_bands == -1:
                # Apply background subtraction
                fg_mask = bg_subtractor.apply(frame)
            else:
                fg_mask = bg_subtractor.apply(frame[:,:,input_bands])
            
            bands = []
            for i in range(len(output_bands)):
                if output_bands[i]:
                    bands.append(fg_mask)
                else:
                    bands.append(frame[:,:,i])
                    
            # Write the frame with temporal filtering to the output video
            out.write(cv2.merge(bands))

            # Print the progress
            frame_count += 1
            bar()

    print("Background subtraction complete.")

    cap.release()
    out.release()
