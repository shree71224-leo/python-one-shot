import json
import os
import shutil
import random

# -----------------------------
# Paths
# -----------------------------

json_file = "instances_all.json"
images_folder = "rendered_pages"

dataset_folder = "dataset"

train_images = os.path.join(dataset_folder, "images", "train")
val_images = os.path.join(dataset_folder, "images", "val")

train_labels = os.path.join(dataset_folder, "labels", "train")
val_labels = os.path.join(dataset_folder, "labels", "val")

# Create folders
for folder in [train_images, val_images, train_labels, val_labels]:
    os.makedirs(folder, exist_ok=True)

# -----------------------------
# Read JSON
# -----------------------------

with open(json_file, "r") as file:
    data = json.load(file)

# -----------------------------
# Create image information
# -----------------------------

images = {}

for image in data["images"]:
    images[image["id"]] = image

# -----------------------------
# Group annotations by image
# -----------------------------

annotations_by_image = {}

for annotation in data["annotations"]:
    image_id = annotation["image_id"]

    if image_id not in annotations_by_image:
        annotations_by_image[image_id] = []

    annotations_by_image[image_id].append(annotation)

# -----------------------------
# Train / validation split
# -----------------------------

# -----------------------------
# Train / validation split
# -----------------------------

# Keep rare classes in training.
# We manually select validation pages
# because some classes occur on only one page.

val_pages = {
    1,
    8,
    21,
    24
}

train_ids = []
val_ids = []

for image_id, image_info in images.items():

    page_number = image_info["page"]

    if page_number in val_pages:
        val_ids.append(image_id)
    else:
        train_ids.append(image_id)

print("Training pages:", len(train_ids))
print("Validation pages:", len(val_ids))

# -----------------------------
# Convert COCO bbox to YOLO
# -----------------------------

def convert_bbox(bbox, image_width, image_height):

    x, y, width, height = bbox

    center_x = x + width / 2
    center_y = y + height / 2

    center_x = center_x / image_width
    center_y = center_y / image_height

    width = width / image_width
    height = height / image_height

    return center_x, center_y, width, height


# -----------------------------
# Process images
# -----------------------------

def process_images(image_ids, image_folder, label_folder):

    for image_id in image_ids:

        image_info = images[image_id]

        page_number = image_info["page"]

        source_image = os.path.join(
            images_folder,
            f"page_{page_number}.png"
        )

        destination_image = os.path.join(
            image_folder,
            f"page_{page_number}.png"
        )

        # Copy image
        shutil.copy2(source_image, destination_image)

        # Create label file
        label_file = os.path.join(
            label_folder,
            f"page_{page_number}.txt"
        )

        with open(label_file, "w") as file:

            for annotation in annotations_by_image[image_id]:

                bbox = annotation["bbox"]

                category_id = annotation["category_id"]

                # YOLO classes start from 0
                class_id = category_id - 1

                x, y, width, height = convert_bbox(
                    bbox,
                    image_info["width"],
                    image_info["height"]
                )

                file.write(
                    f"{class_id} {x} {y} {width} {height}\n"
                )


# Process training images
process_images(
    train_ids,
    train_images,
    train_labels
)

# Process validation images
process_images(
    val_ids,
    val_images,
    val_labels
)

print("Dataset conversion completed!")

print("Training images:", len(train_ids))
print("Validation images:", len(val_ids))

print("YOLO dataset created inside:", dataset_folder)