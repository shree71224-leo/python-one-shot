import os
import json
from PIL import Image

# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

IMAGE_FOLDER = "rendered_pages"
JSON_FILE = "instances_all.json"

OUTPUT_FOLDER = "tiled_dataset"

TILE_SIZE = 640
OVERLAP = 0.20

# --------------------------------------------------
# CREATE OUTPUT FOLDERS
# --------------------------------------------------

train_images = os.path.join(
    OUTPUT_FOLDER, "images", "train"
)

val_images = os.path.join(
    OUTPUT_FOLDER, "images", "val"
)

train_labels = os.path.join(
    OUTPUT_FOLDER, "labels", "train"
)

val_labels = os.path.join(
    OUTPUT_FOLDER, "labels", "val"
)

for folder in [
    train_images,
    val_images,
    train_labels,
    val_labels
]:
    os.makedirs(folder, exist_ok=True)

# --------------------------------------------------
# LOAD JSON
# --------------------------------------------------

with open(JSON_FILE, "r") as file:
    data = json.load(file)

# --------------------------------------------------
# IMAGE INFORMATION
# --------------------------------------------------

images = {}

for image in data["images"]:
    images[image["id"]] = image

# --------------------------------------------------
# GROUP ANNOTATIONS BY IMAGE
# --------------------------------------------------

annotations_by_image = {}

for annotation in data["annotations"]:

    image_id = annotation["image_id"]

    if image_id not in annotations_by_image:
        annotations_by_image[image_id] = []

    annotations_by_image[image_id].append(annotation)

# --------------------------------------------------
# VALIDATION PAGES
# --------------------------------------------------

val_pages = {
    1,
    8,
    21,
    24
}

# --------------------------------------------------
# TILE SETTINGS
# --------------------------------------------------

step = int(TILE_SIZE * (1 - OVERLAP))

print("Tile size:", TILE_SIZE)
print("Overlap:", OVERLAP)
print("Step:", step)

# --------------------------------------------------
# PROCESS EACH ANNOTATED PAGE
# --------------------------------------------------

for image_id, image_info in images.items():

    page_number = image_info["page"]

    # Only process pages that have annotations
    if image_id not in annotations_by_image:
        continue

    image_path = os.path.join(
        IMAGE_FOLDER,
        f"page_{page_number}.png"
    )

    if not os.path.exists(image_path):
        print("Missing image:", image_path)
        continue

    image = Image.open(image_path)

    image_width, image_height = image.size

    annotations = annotations_by_image[image_id]

    # Decide train or validation
    if page_number in val_pages:
        image_output = val_images
        label_output = val_labels
    else:
        image_output = train_images
        label_output = train_labels

    # --------------------------------------------------
    # CREATE TILES
    # --------------------------------------------------

    tile_number = 0

    for y in range(0, image_height, step):

        for x in range(0, image_width, step):

            x2 = min(x + TILE_SIZE, image_width)
            y2 = min(y + TILE_SIZE, image_height)

            # Actual tile dimensions
            tile_width = x2 - x
            tile_height = y2 - y

            # Skip very small edge tiles
            if tile_width < TILE_SIZE * 0.5:
                continue

            if tile_height < TILE_SIZE * 0.5:
                continue

            tile = image.crop(
                (x, y, x2, y2)
            )

            tile_name = (
                f"page_{page_number}_"
                f"tile_{tile_number}"
            )

            image_file = os.path.join(
                image_output,
                tile_name + ".png"
            )

            label_file = os.path.join(
                label_output,
                tile_name + ".txt"
            )

            # --------------------------------------------------
            # FIND OBJECTS INSIDE TILE
            # --------------------------------------------------

            yolo_labels = []

            for annotation in annotations:

                category_id = annotation["category_id"]

                bbox = annotation["bbox"]

                bx, by, bw, bh = bbox

                bx2 = bx + bw
                by2 = by + bh

                # Object center
                center_x_original = bx + bw / 2
                center_y_original = by + bh / 2

                # Keep object if its CENTER is inside tile
                if not (
                    x <= center_x_original < x2
                    and
                    y <= center_y_original < y2
                ):
                    continue

                # Convert coordinates relative to tile
                center_x = (
                    center_x_original - x
                )

                center_y = (
                    center_y_original - y
                )

                # Normalize to tile
                center_x /= tile_width
                center_y /= tile_height

                width = bw / tile_width
                height = bh / tile_height

                class_id = category_id - 1

                yolo_labels.append(
                    f"{class_id} "
                    f"{center_x:.6f} "
                    f"{center_y:.6f} "
                    f"{width:.6f} "
                    f"{height:.6f}"
                )

            # --------------------------------------------------
            # SAVE ONLY TILES WITH OBJECTS
            # --------------------------------------------------

            if len(yolo_labels) == 0:
                continue

            tile.save(image_file)

            with open(label_file, "w") as file:

                for label in yolo_labels:
                    file.write(label + "\n")

            tile_number += 1

    print(
        f"Page {page_number}: "
        f"processed"
    )

print()
print("================================")
print("TILING COMPLETED")
print("================================")
print("Output:", OUTPUT_FOLDER)