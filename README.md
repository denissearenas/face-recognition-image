# face_recognition_image
Recognize faces and and tag names using face_recognition library

# Folder Structure

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

`Workingfolder` contains all the images needed to tag images.
`TrainingImages` contains the images of people we want to use to train the model. Basically the people we want to tag later. It´s Important the name of the image is the name of the person in it. 
`TestImages` contains the images we want to detect faces and tag people. 
`OutputImages` will contain the TestImages with the faces tagged after the script is run.