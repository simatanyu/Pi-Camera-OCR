import cv2
from PIL import Image
import pytesseract
import pandas as pd
import os
import time
from datetime import datetime
import matplotlib.pyplot as plt
import threading
import numpy as np

# Path to the folder containing images
folder_path = "/Users/gao/Desktop/April1"
output_file = "/Users/gao/Desktop/Extracted_Numbers.csv"

# Tesseract OCR Configuration
# psm-7: Target is a line of horizontal words
# oem-3: Mixed mode, used data with neural network and exist data
# White list: Only recognize the words on this list
myconfig = r"--psm 7 --oem 3 -l nml2 -c tessedit_char_whitelist=0123456789."

# Global variables
processed_images = set()
results_array = []  # Array to store processed image results in memory
visualization_img = None

# Initialize an empty plot
fig, ax = plt.subplots()

# Function to write results to CSV
def save_results_to_csv(output_file):
    global processed_images, results_array, visualization_img
    if results_array:  # Only save if there's data
        data = pd.DataFrame(results_array)
        data.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")

# Function to process images in the folder
def process_images(folder_path):
    global processed_images, results_array, visualization_img

    x, y, w, h = 183, 155, 242, 105  # Crop Region

    block_size = 45  # The size of the color block for reverse fillingw
    adaptive_c = 4
    #scale_factor = 2 # Scale the image to specific size for better recognition

    image_files = sorted(os.listdir(folder_path))
    for image_file in image_files:
        if image_file in processed_images:
            continue

        image_path = os.path.join(folder_path, image_file)
        if image_path.endswith((".png", ".jpg", ".jpeg")):
            image = cv2.imread(image_path)
            if image is None:
                continue

            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            roi = gray_image[y:y + h, x:x + w]  # Crop for grey scale
            #roi = cv2.resize(roi, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

            im_bw = cv2.adaptiveThreshold(
                roi, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY_INV,  #  Inverse mode, Depend on the contrast between targets and background
                block_size,
                adaptive_c
            )
            im_bw = cv2.medianBlur(im_bw, 9)  # Background noise / blur
            kernel = np.ones((3, 3), np.uint8)
            im_bw = cv2.dilate(im_bw, kernel, iterations=1)  # Dilate the identified pixel blocks

            pil_image = Image.fromarray(im_bw)
            text = pytesseract.image_to_string(pil_image, config=myconfig) # Call for tesseract
            numbers = "".join([char for char in text if char.isdigit() or char == '.'])

            vis_img = cv2.cvtColor(im_bw, cv2.COLOR_GRAY2BGR)
            vis_img[vis_img == 255] = 0

            cv2.putText(vis_img, f"Result: {numbers}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            visualization_img = vis_img.copy()

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result = {
                "Timestamp": timestamp,
                "Image File": image_file,
                "Extracted Numbers": numbers
            }

            results_array.append(result)  # Store the result in memory
            processed_images.add(image_file)  # Mark as processed, in case do test run for multiple times but the same samples


            print(f"Processed: {image_file}")
            print(numbers)

# Function to start processing images in a separate thread
def start_processing():
    max_checks = 1  # Check up to 10 times for new images
    check_count = 0
    last_save_time = time.time()  # Record the last save time

    while check_count < max_checks:
        process_images(folder_path)

        # Save results to CSV every 5 minutes
        if time.time() - last_save_time >= 20:  # Test Time set up
            save_results_to_csv(output_file)
            last_save_time = time.time()

        # Exit if no new images are found
        if len(os.listdir(folder_path)) == 0:
            print("No new images detected. Exiting processing loop.")
            save_results_to_csv(output_file)  # Save final results
            break

        time.sleep(3)
        check_count += 1

# Recognition result display
def update_visualization():
    cv2.namedWindow('OCR Processing Preview', cv2.WINDOW_NORMAL)
    while True:
        if visualization_img is not None:
            # cv2 window display
            cv2.imshow('OCR Processing Preview', visualization_img)
            # Size of display window
            cv2.resizeWindow('OCR Processing Preview', 800, 600)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        time.sleep(5)  # Wait time for each image


# Start image processing in a separate thread
processing_thread = threading.Thread(target=start_processing)
processing_thread.start()

visualization_thread = threading.Thread(target=update_visualization, daemon=True)
visualization_thread.start()

# Ensure the processing thread completes
processing_thread.join()