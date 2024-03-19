import argparse
import os
import shutil

def copy_dataset(formatted_number):
    dataset_dir = f"/scratch/tmp/jdanel/data/datasets/complete_{formatted_number}"

    print(f"Build a dataset for: {formatted_number}")
    
    # Create directory structure
    os.makedirs(os.path.join(dataset_dir, "train", "images"))
    os.makedirs(os.path.join(dataset_dir, "train", "labels"))
    os.makedirs(os.path.join(dataset_dir, "val", "images"))
    os.makedirs(os.path.join(dataset_dir, "val", "labels"))

    # Copy data.yaml file
    shutil.copy("/scratch/tmp/jdanel/data/datasets/original/data.yaml", os.path.join(dataset_dir, "data.yaml"))

    # Copy images and labels
    img_source_dir = "/scratch/tmp/jdanel/data/datasets/complete/data/images"
    label_source_dir = "/scratch/tmp/jdanel/data/datasets/complete/data/labels"

    img_val_dest_dir = os.path.join(dataset_dir, "val", "images")
    label_val_dest_dir = os.path.join(dataset_dir, "val", "labels")

    img_train_dest_dir = os.path.join(dataset_dir, "train", "images")
    label_train_dest_dir = os.path.join(dataset_dir, "train", "labels")

    img_files = [f"img_{formatted_number}{ext}" for ext in ["", ".png", ".jpg", ".jpeg"]]
    label_files = [f"label_{formatted_number}{ext}" for ext in [".txt"]]

    for img_file in img_files:
        shutil.copy(os.path.join(img_source_dir, img_file), img_val_dest_dir)

    for label_file in label_files:
        shutil.copy(os.path.join(label_source_dir, label_file), label_val_dest_dir)
        shutil.copy(os.path.join(label_source_dir, label_file), label_train_dest_dir)

def main():
    parser = argparse.ArgumentParser(description="Build a dataset")
    parser.add_argument("--formatted_number", required=True, help="Formatted number for the dataset")

    args = parser.parse_args()

    copy_dataset(args.formatted_number)

if __name__ == "__main__":
    main()
