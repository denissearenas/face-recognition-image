# Face Recognition Image
Recognize faces and and tag names using face_recognition library

## Folder Structure

```
project
├───.metadata
├───logs
├───Workingfolder
│   ├───OutputImages
│   ├───TestImages
│   └───TrainingImages
├───main.py
├───imageRecognition.py
└───logging_config.ini
```

1. `.metadata` will be use to store the faces_encoding

2. `Workingfolder` contains all the images needed to tag images.

    - `TrainingImages` contains the images of people we want to use to train the model. Basically the people we want to tag later. It´s Important the name of the image is the name of the person in it. 

    - `TestImages` contains the images we want to detect faces and tag people. 

    - `OutputImages` will contain the TestImages with the faces tagged after the script is run.

## Usage 

1. Add into `Workingfolder/TrainingImages` one image for each person to tag. The name of the image is the name used later to tag that person. 

2. Add into `Workingfolder/TestImages` the images to tag people in. 

3. Run `main.py`

## Colors

Depending on the distance there is a color code for the rectangles drawn. By default the tolerance is 0.6 and the colors as set as a proportion of the tolerance. Then by default this are the color codes:

- <span style="background-color:#606060"> Grey </span>
```
Unknown
distance > tolerance 
default: distance > 0.60
```

- <span style="background-color:#640000"> Red </span> 

```
distance > tolerance*0.84 
[default: distance >= 0.60*0.84 => distance >= 0.504]
```

- <span style="background-color:#ff8000"> Orange </span> 

```
distance >= tolerance*0.68
[default: distance >= 0.60*0.68 => distance >= 0.408]
```

- <span style="background-color:#006400"> Green </span> 

```
distance < tolerance*0.68
[default: distance < 0.60*0.68 => distance < 0.408]
```


## Credits 
- https://github.com/Lazymindz/MeetupMemberImageTag
- https://github.com/ageitgey/face_recognition/blob/master/examples/recognize_faces_in_pictures.py
- https://github.com/ageitgey/face_recognition
- https://github.com/davisking/dlib


