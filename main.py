import logging
from logging.config import fileConfig

import os, os.path

import imageRecognition


#Test Folder
TestFolder = 'WorkingFolder/TestImages/'

# Create the Working folders
working_folders = ['logs','.metadata','WorkingFolder','./Workingfolder/OutputImages']
[os.makedirs(folder) for folder in working_folders if not os.path.exists(folder)]


# Load log config
fileConfig('logging_config.ini')
logger = logging.getLogger()


if __name__ == "__main__":
        
    encodings = imageRecognition.loadEncodings()

    if len(os.listdir(TestFolder)) > 0:
        for file in os.listdir(TestFolder):
            name_image = os.path.join(TestFolder,file)
            filename = 'output'
            if file.rfind('.') >= 0:
                filename = file[:file.rfind('.')]
            imageRecognition.tagPeople_cv2(TestFolder+file, encodings, tolerance=0.60, output_filename = filename)

        


