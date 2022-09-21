import cv2
import os

face_classifier = cv2.CascadeClassifier("application/haarcascade_frontalface_default.xml")

#cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)

def cropping(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(
        gray,
        scaleFactor = 1.1,
        minNeighbors = 5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

    if faces is None:
        return None
    
    cropped = 0
    for (x, y, w, h) in faces:
        cropped = image[y:y+h, x:x+w]

    return cropped
