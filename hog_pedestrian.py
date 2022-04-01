import sys
import random
import numpy as np
import cv2


# Video
cap = cv2.VideoCapture('.avi')

if not cap.isOpened():
    print('Video open failed!')
    sys.exit()

# HOG descriptor to detect pedestrian
hog = cv2.HOGDescriptor()

hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector()) 
# 보행자 검출 기능 svm coefficient value

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Detect pedestrian for each frame
    detected, _ = hog.detectMultiScale(frame)

    # Indicate result on the screen
    for (x, y, w, h) in detected:
        c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        cv2.rectangle(frame, (x, y, w, h), c, 2)

    cv2.imshow('frame', frame)
    if cv2.waitKey(10) == 27:
        break

cv2.destroyAllWindows()
