from ultralytics import YOLO
import cv2
import os

# Load YOLO model
model = YOLO("yolo26n.pt")

# Input image
image_path = "input.png"

# Run YOLO detection
results = model(
    source=image_path,
    conf=0.25
)

# Get the result
result = results[0]

# Create output folder
os.makedirs("outputs", exist_ok=True)

# Draw detected objects on the image
annotated_image = result.plot()

# Save the result
cv2.imwrite(
    "outputs/detected.png",
    annotated_image
)

print("Detection completed!")
print("Output saved as outputs/detected.png")