# Raspeberry Pi camera and OCR
This project developed for raspeberry Pi and low resolution camera. By using Tesseract 4.0 trained tessdata to recognize 7 segment fonts. This project can also be used with "OCR-Web-Graph".  

**nml.trainedata** 
*Char train = 2.553%, word train = 4.5%*

**Capturer.py**  
A simple script to control the raspberry Pi camera by using library Picamera2

**OCR.py**  
Script for optical character recognize, including images process (Crop, Dilate, Adaptive, Blur)

**Capturer+OCR.py**  
An integrated program can be used directly by people with the same usage environment.

## Tesseract 4.0 Trainning Procedure
