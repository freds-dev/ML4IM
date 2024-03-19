from PIL import Image

offset = 0.02
frame_size = 10  # Adjust the frame size as needed

def stack_images(image_paths, output_path):
    # Open the first image to get dimensions
    base_image = Image.open(image_paths[0])
    width, height = base_image.size
    
    # Calculate the new dimensions considering the frame
    new_width = int(width + ((len(image_paths) - 1) * offset * width) + 2 * frame_size)
    new_height = int(height + ((len(image_paths) - 1) * offset * height) + 2 * frame_size)
    
    # Create a new image with transparent background
    stacked_image = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
    
    # Paste each image with a diagonal offset and a black frame
    for i, image_path in enumerate(image_paths):
        print(f"{i} of {len(image_paths)} processed")
        image = Image.open(image_path)
        
        # Create a new image with a black frame
        framed_image = Image.new("RGBA", (width + 2 * frame_size, height + 2 * frame_size), (0, 0, 0, 255))
        framed_image.paste(image, (frame_size, frame_size))

        # Calculate offset (5% of width and height)
        offset_x = int(offset * width * (len(image_paths) - 1 - i) + frame_size)  # Updated offset calculation
        offset_y = int(offset * height * (len(image_paths) - 1 - i) + frame_size)  # Updated offset calculation

        # Paste the framed image onto the stacked image with alpha channel
        stacked_image.paste(framed_image, (offset_x, offset_y), framed_image)

    # Save the result
    stacked_image.save(output_path)

def create_file_name(frame_number):
    return f"{frame_number:05d}.jpg"

def create_frame_paths(dir, min_frame, max_frame):
    return [f"{dir}/{create_file_name(frame_number)}" for frame_number in range(min_frame, max_frame + 1)]

if __name__ == "__main__":
    # Example usage
    input_dir = "../../data/frames/one"
    inputs = create_frame_paths(input_dir, 1411, 1421)
    output_image = "stacked_image_with_frame.png"
    stack_images(inputs, output_image)
