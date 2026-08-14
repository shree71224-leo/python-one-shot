from PIL import Image, ImageDraw
import os

image_path = "tiled_dataset/images/train/page_22_tile_0.png"
label_path = "tiled_dataset/labels/train/page_22_tile_0.txt"

image = Image.open(image_path).convert("RGB")
draw = ImageDraw.Draw(image)

width, height = image.size

with open(label_path, "r") as f:
    for line in f:
        parts = line.strip().split()

        if len(parts) != 5:
            continue

        class_id, cx, cy, w, h = map(float, parts)

        cx *= width
        cy *= height
        w *= width
        h *= height

        x1 = int(cx - w / 2)
        y1 = int(cy - h / 2)
        x2 = int(cx + w / 2)
        y2 = int(cy + h / 2)

        draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
        draw.text((x1, y1 - 15), str(int(class_id)), fill="red")

os.makedirs("outputs", exist_ok=True)

output = "outputs/page_22_tile_0_labels.jpg"
image.save(output)

print("Saved:", output)