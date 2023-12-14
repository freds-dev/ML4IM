import cv2
import os

def draw_bounding_boxes(images_folder, labels_folder, output_folder):
    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Process each image
    for filename in os.listdir(images_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(images_folder, filename)
            img = cv2.imread(img_path)

            # Load corresponding YOLO label file
            label_path = os.path.join(labels_folder, os.path.splitext(filename)[0] + '.txt')

            if os.path.exists(label_path):
                with open(label_path, 'r') as label_file:
                    lines = label_file.readlines()

                    for line in lines:
                        # Parse YOLO format: <class_id> <center_x> <center_y> <width> <height>
                        class_id, center_x, center_y, width, height = map(float, line.strip().split())

                        # Convert YOLO format to OpenCV format: (x, y, w, h)
                        x = int((center_x - width / 2) * img.shape[1])
                        y = int((center_y - height / 2) * img.shape[0])
                        w = int(width * img.shape[1])
                        h = int(height * img.shape[0])

                        bbox_color = (0, 255, 0)  # Green color for bounding boxes

                        # Draw bounding box
                        cv2.rectangle(img, (x, y), (x + w, y + h), bbox_color, 2)

                # Save the image with bounding boxes
                output_path = os.path.join(output_folder, f"annotated_{filename}")
                print(f"annotated_{filename}")
                cv2.imwrite(output_path, img)

if __name__ == "__main__":
    # Replace these paths with your actual paths
    images_folder = '../../data/datasets/test_cropping_final/train/images'
    labels_folder = '../../data/datasets/test_cropping_final/train/labels'
    output_folder = '../../tmp/check_bb_final'

    draw_bounding_boxes(images_folder, labels_folder, output_folder)
