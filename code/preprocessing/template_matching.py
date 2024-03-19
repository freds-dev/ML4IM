import cv2
import os
import numpy as np
import random

def load_random_images(directory, n):
    """
    Load n random images from the specified directory.

    Parameters:
    - directory (str): Path to the directory containing images.
    - n (int): Number of random images to load.

    Returns:
    - List of loaded images.
    """

    # Get a list of all files in the directory
    all_files = os.listdir(directory)

    # Filter only image files (you may need to extend the list of valid image extensions)
    image_files = [f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # Ensure that there are enough images in the directory
    if len(image_files) < n:
        raise ValueError("Not enough images in the directory.")

    # Choose n random images
    selected_images = random.sample(image_files, n)

    # Load the selected images
    loaded_images = []
    for image_file in selected_images:
        image_path = os.path.join(directory, image_file)
        image = cv2.imread(image_path)

        if image is not None:
            loaded_images.append(image)
        else:
            print(f"Error loading image: {image_path}")

    return loaded_images

def template_matching(input_path, output_path, threshold = 0.5):
    """
    Apply template matching to frames in a video using multiple templates and count matches above a threshold.

    Parameters:
    - input_path (str): Path to the input video.
    - template_directory (str): Path to the directory containing template images.
    - output_path (str): Path to save the output video.
    - threshold (float): Threshold for considering a match.

    Returns:
    - None
    """

    # Load templates using load_random_images
    templates = load_random_images("./clips", n=3)

    if not templates:
        print("Error: No valid templates loaded.")
        return

    # Open the video
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Get video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Create VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=True)

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to grayscale
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      
        

        # Count the number of matches above the threshold for each template
        frames = []
        for template in templates:
            # Ensure consistent depth and type for the template and the frame
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            #print(f"frame gray shape: {frame_gray.shape}")
            #print(f"template shape: {template.shape}")
            result = cv2.matchTemplate(frame_gray, template, cv2.TM_CCOEFF_NORMED)
            #print(f"result shape: {result.shape}")
            max = np.amax(result)
            frame = result * (255/max)
            frame = frame.astype("uint8")
            frames.append(cv2.copyMakeBorder(frame, template.shape[0], template.shape[0], template.shape[1], template.shape[1], cv2.BORDER_CONSTANT, value=0))


        for f in frames:
            print(frame.shape)

        
        # Save the resulting frame
        out.write(cv2.merge(frames))

        # Print the progress
        print(f"{frame_count}/{total_frames}")
        frame_count += 1
        

    print("Template matching complete.")

    cap.release()
    out.release()

