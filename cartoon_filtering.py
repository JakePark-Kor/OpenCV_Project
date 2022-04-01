# 카툰 필터 카메라

from re import L
import sys
import numpy as np
import cv2


def cartoon_filter(img):
    h, w = img.shape[:2]
    img =  cv2.resize(img, (w//2, h//2))
    blr = cv2.bilateralFilter(img, -1, 20, 7)
    edge = 255 - cv2.Canny(img, 50, 200)
    #Grayscale로 반환되므로, 컬러로 바꿔야 blr와 결합가능
    edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

    dst = cv2.bitwise_and(blr, edge)
    #dst = cv2.resize(dst, (w, h), interpolation = cv2.INTER_NEAREST)


    return dst
 

def pencil_sketch(img):
    h, w = img.shape[:2]
    img =  cv2.resize(img, (w//2, h//2))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blr = cv2.GaussianBlur(gray, (0, 0), 3)
    dst = cv2.divide(gray, blr, scale= 255)
    dst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)

    return dst


cap = cv2.VideoCapture('.mp4')
# You can give either a video file or 0
# If you set 0, it turns your front camera in your computer on 

if not cap.isOpened():
    print('Try again')
    sys.exit()

cam_mode = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    if cam_mode == 1:
        frame = cartoon_filter(frame)
    elif cam_mode == 2:
        frame = pencil_sketch(frame)
 
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)

    
    if key == 27: # Esc to shut down
        break
    elif key == ord(' '): # space bar to change the mode 
        cam_mode += 1
        if cam_mode == 3: # return to the origin.
            cam_mode = 0

cap.release()
cv2.destroyAllWindows()
