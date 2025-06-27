from picamera2 import Picamera2
from datetime import datetime
import os
from PIL import Image

# Configuration
save_directory = "New folder"  # Change to your target folder
capture_count = 10  # Number of images to capture
capture_interval = 1  # Interval in seconds between captures

# Ensure the save directory exists
os.makedirs(save_directory, exist_ok=True)

# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()

print(f"Loading～ {save_directory}")

# Capture images in a loop
for i in range(capture_count):
    # Capture the image
    image = picam2.capture_array()

    # Generate a filename with a timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}.jpg"
    file_path = os.path.join(save_directory, filename)

    # Save the image
    im = Image.fromarray(image)
    im.save(file_path)

    print(f"Captured and saved image {i + 1}/{capture_count}: {file_path}")

    # Wait for the specified interval before capturing the next image
    if i < capture_count - 1:
        time.sleep(capture_interval)

# Stop the camera
picam2.stop()
print("Done")
