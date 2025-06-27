# Raspeberry Pi camera and OCR
This project developed for raspeberry Pi and low resolution camera. By using Tesseract 4.0 trained tessdata to recognize 7 segment fonts. This project can also be used with "OCR-Web-Graph".  

**nml.trainedata (2000 iterations check point)**  
*Char train = 2.553%, word train = 4.5%*

**Capturer.py**  
A simple script to control the raspberry Pi camera by using library Picamera2

**OCR.py**  
Script for optical character recognize, including images process (Crop, Dilate, Adaptive, Blur)

**Capturer+OCR.py**  
An integrated program can be used directly by people with the same usage environment.

## Tesseract 4.0 Trainning Procedure (Windows)  
Required tool *Tesseract 4.1, jtessboxeditor, images samples, eng-trainneddata(must be lstm)*  
1. Add the *bin* directory to the system variable Path  
2. Add *tessdata* (trained font file) to the administrator user variable, variable name TESSDATA_PREFIX, variable value is the path of tessdata directory  
3. Convert to image samples to *tif* file. This is can be done by jtessboxeditor  
   Tools - Merge TIFF  
4. Generate .box file through eng-trainnedata  
   ex. tesseract eng.myfont.exp0.tif eng.myfont.exp0 -l eng --psm 7 batch.nochop makebox
   form: tesseract (name of .tif file) (Name of generated file, no suffix required) -l (Used trainedata) --psm (mode number) batch.nochop makebox  
5. Open box file through jtessboxeditor  
6. Use jtessboxeditor manual proofreading of the recognition range and correct recognition results  
7. Generate .lstm file through eng-trainneddata  
   ex: combine_tessdata -e eng.trainedata eng.lstm  
   form: combine_tessdata -e (Name of traineddata) (Name of extracted .lstm file)  
8. Use .tif and .box files to generate .lstmf file  
   form: tesseract (Name of .tif file) (Name of .lstmf file) -l (The name of used traineddata) --psm (mode number) lstm.train  
9. Train  
   form: lstmtraining  
   --model_output (Output directory)  
   --continue from (Continue training from check point or lstmf file)  
   --traineddata (Name of used traineddata)  
   --debug_interval -1 (Default, return the result of training)  
   --max_iterations (Times of training)  
10. Combine check point and .traineddata to generate new font
   lstmtraining --stop_training  
   --continue_from (Best check point with lowest error rate)  
   --model_output (Name of new .traineddata file)

   
