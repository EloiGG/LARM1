import cv2
import numpy as np

cap=cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    image=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier('/Users/gabrielharivel/IMT/NU/LARM/cascade2.xml')

    detected_faces = face_cascade.detectMultiScale(image, scaleFactor=1.10, minNeighbors=3)

    for (column, row, width, height) in detected_faces:
        cv2.rectangle(frame ,( column, row) , (column + width, row + height) , (0, 255, 0) , 2)

    cv2.imshow('Image', frame)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break