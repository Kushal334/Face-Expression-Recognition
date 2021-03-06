#Importing the relevant library
import cv2
from model import FacialExpressionModel
import numpy as np

#Following function detects faces
facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = FacialExpressionModel("model.json", "model_weights.h5") # loading our model
font = cv2.FONT_HERSHEY_SIMPLEX

class VideoCamera(object):
    def __init__(self):
        #Initialising video capturing function, pointing opencv to a video already stored
        self.video = cv2.VideoCapture("/home/rhyme/Desktop/Project/videos/facial_exp.mkv")
        #self.video = cv2.VideoCapture(0) # I am initialising the user webcam here instead of passing a default #file
        #change to 0 -> for default webcam

    def __del__(self):
        self.video.release()

    # returns camera frames along with bounding boxes and predictions
    def get_frame(self):
        _, fr = self.video.read()
        #Make sure each input frame is in GRAYSCALE
        gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        faces = facec.detectMultiScale(gray_fr, 1.3, 5)

        for (x, y, w, h) in faces:
            fc = gray_fr[y:y+h, x:x+w]

            roi = cv2.resize(fc, (48, 48))
            #Here, we predict 
            pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])

            cv2.putText(fr, pred, (x, y), font, 1, (255, 255, 0), 2)
            #Add a bounding box to concentrate on the deciding feature
            cv2.rectangle(fr,(x,y),(x+w,y+h),(255,0,0),2)
        #finally return the image to main.py
        _, jpeg = cv2.imencode('.jpg', fr)
        return jpeg.tobytes()
