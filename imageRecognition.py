import face_recognition
from PIL import Image, ImageDraw, ImageFont
import os, os.path
import time
import numpy as np
import cv2

# This is an example of running face recognition on a single image
# and drawing a box around each person that was identified.
# Code skeleton from https://github.com/ageitgey/face_recognition/blob/master/examples/recognize_faces_in_pictures.py

# Load a sample picture and learn how to recognize it.
def createAndLoadEncodings():
    loaded_face_encodings = {}
    if len(os.listdir('WorkingFolder/TrainingImages')) > 0:
        for file in os.listdir('WorkingFolder/TrainingImages'):
            name = file
            if file.rfind('.') >= 0:
                #remove file extension from name
                name = file[:file.rfind('.')]
            name_image = face_recognition.load_image_file(os.path.join('WorkingFolder/TrainingImages',file))
            name_face_encoding = face_recognition.face_encodings(name_image)
            if len(name_face_encoding) > 0:
                loaded_face_encodings[name] = name_face_encoding[0]
    np.save('./.metadata/faces_encoding.npy', loaded_face_encodings)
    return np.load('./.metadata/faces_encoding.npy')

def loadEncodings(retrain=False):
    if (not os.path.exists('./.metadata/faces_encoding.npy')) or (retrain==True):
        return createAndLoadEncodings()
    else:
        return np.load('./.metadata/faces_encoding.npy')


def tagPeople_pil(input_image, loaded_face_encodings, tolerance=0.60, output_filename = 'output'):

    known_face_names, known_face_encodings = list(loaded_face_encodings[()].keys()), list(loaded_face_encodings[()].values())

    # Load an image with an unknown face
    unknown_image = face_recognition.load_image_file(input_image)
    
    # Find all the faces and face encodings in the unknown image
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
    # See http://pillow.readthedocs.io/ for more about PIL/Pillow
    pil_image = Image.fromarray(unknown_image)
    
    # Create a pil_imageillow ImageDraw Draw instance to draw with
    draw = ImageDraw.Draw(pil_image)

    # Loop through each face found in the unknown image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=tolerance)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        name = "Unknown"
        color = (96, 96, 96)    #grey
        min_face_distances = min(face_distances)
        distance = str(round(min_face_distances,3))

        #% of tolerance to change color:
        tolerance_red = tolerance*0.84
        tolerance_orange = tolerance*0.68

        # If a match was found in known_face_encodings, use the one with the minimun distance 
        if True in matches:
            #get index of minimun distance
            match_index = np.argmin(face_distances)
            name = known_face_names[match_index]
            if min_face_distances >= tolerance_red:
                color = (100, 0, 0)
            elif min_face_distances >= tolerance_orange:
                color = (255, 128, 0)
            else:
                color = (0,100,0)
        name =  name + ' - ' + distance

        # Draw 4 (rectangle_width) boxes around the face using the Pillow module
        rectangle_width = 4
        for i in range(rectangle_width):
            draw.rectangle(((left - i, top - i), (right + i, bottom + i )), outline=color)
        
        text_width, text_height = draw.textsize(name)
        
        #offset: extra lengh needed in each side to fit the name.
        offset = 0
        #If Label is longer than rectangle width, calculate offset needed. 
        if ( right-left ) < text_width :
            offset =  (text_width - ( right - left ))/2
        
        draw.rectangle(((left - offset - rectangle_width +1, bottom + text_height + 10), (right + offset + rectangle_width -1, bottom)), fill=color, outline=color)
        draw.text((left - offset , bottom + text_height - 5 ), name, fill=(255, 255, 255, 255))

    # Remove the drawing library from memory as per the Pillow docs
    del draw

    # Save a copy of the new image to disk
    timestring = time.strftime("%Y%m%d_%H%M%S")
    pil_image.save(f"./WorkingFolder/OutputImages/{output_filename}_{timestring}.PNG", "PNG")


def tagPeople_cv2(input_image, loaded_face_encodings, tolerance=0.60, output_filename = 'output'):
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 0.5
    known_face_names, known_face_encodings = list(loaded_face_encodings[()].keys()), list(loaded_face_encodings[()].values())

    # Load an image with an unknown face
    unknown_image = face_recognition.load_image_file(input_image)
    
    # Find all the faces and face encodings in the unknown image
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

     #Load the input_image using OpenCV2
    cv2_image = cv2.imread(input_image)


    # Loop through each face found in the unknown image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=tolerance)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        name = "Unknown"
        color = (96, 96, 96) #grey
        min_face_distances = min(face_distances)
        distance = str(round(min_face_distances,3))   

        #% of tolerance to change color:
        tolerance_red = tolerance*0.85
        tolerance_orange = tolerance*0.68

        # If a match was found in known_face_encodings, use the one with the minimun distance 
        if True in matches:
            #get index of minimun distance
            match_index = np.argmin(face_distances)            
            name = known_face_names[match_index]
            if min_face_distances >= tolerance_red:
                color = (0, 0, 100)
            elif min_face_distances >= tolerance_orange:
                color = (0, 128, 255)
            else:
                color = (0,100,0)
        
        name =  name + ' - ' + distance

        # Draw a box around the face
        rectangle_width = 4
        cv2.rectangle(cv2_image, (left, top), (right, bottom), color, rectangle_width)

        #get the text width and height for the name, font and font_scale chosen 
        size = cv2.getTextSize(name, font, font_scale, 1)
        text_width = size[0][0]
        text_height = size[0][1]
        
        #offset: extra lengh needed in each side to fit the name.
        offset = 0
        #If Label is longer than rectangle width, calculate offset needed. 
        if ( right-left ) < text_width :
            offset =  int((text_width - ( right - left ))/2)

        # Draw a label with a name below the face
        cv2.rectangle(cv2_image, (left-offset-int(rectangle_width/2), bottom + int(text_height*2) ), (right+offset+int(rectangle_width/2), bottom), color, cv2.FILLED)        
        cv2.putText(cv2_image, name, (left -offset, bottom + int(text_height*2) - 6), font, font_scale, (255, 255, 255), 1)

    #save image
    timestring = time.strftime("%Y%m%d_%H%M%S")
    cv2.imwrite("./WorkingFolder/OutputImages/"+output_filename+"_"+timestring+".PNG", cv2_image);
