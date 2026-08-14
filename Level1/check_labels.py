from PIL import Image, ImageDraw

# -----------------------------
# Paths
# -----------------------------

image_path = "dataset/images/train/page_5.png"
label_path = "dataset/labels/train/page_5.txt"
output_path = "outputs/page_5_labels.jpg"

# -----------------------------
# Open image
# -----------------------------

image = Image.open(image_path)
draw = ImageDraw.Draw(image)

image_width, image_height = image.size

# -----------------------------
# Read YOLO labels
# -----------------------------

with open(label_path, "r") as file:
    lines = file.readlines()

# -----------------------------
# Draw bounding boxes
# -----------------------------

for line in lines:

    values = line.strip().split()

    if len(values) != 5:
        continue

    class_id, center_x, center_y, width, height = map(float, values)

    # Convert normalized YOLO coordinates
    center_x *= image_width
    center_y *= image_height
    width *= image_width
    height *= image_height

    # Convert center coordinates to corners
    x1 = center_x - width / 2
    y1 = center_y - height / 2

    x2 = center_x + width / 2
    y2 = center_y + height / 2

    # Draw box
    draw.rectangle(
        [x1, y1, x2, y2],
        outline="red",
        width=3
    )

    # Draw class number
    draw.text(
        (x1, y1 - 15),
        str(int(class_id)),
        fill="red"
    )

# -----------------------------
# Save result
# -----------------------------

image.save(output_path)

print("Labels visualized successfully!")
print("Saved at:", output_path)