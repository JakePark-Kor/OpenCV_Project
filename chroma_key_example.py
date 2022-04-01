import sys
import numpy as np
import cv2


# Color Background
cap1 = cv2.VideoCapture('.mp4')

if not cap1.isOpened():
    print('Video open failed!')
    sys.exit()

# the video you wanna use instead
cap2 = cv2.VideoCapture('.mp4')

if not cap2.isOpened():
    print('video open failed!')
    sys.exit()

# Assume that FPS of two videos are same
w = round(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
h = round(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
frame_cnt1 = round(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
frame_cnt2 = round(cap2.get(cv2.CAP_PROP_FRAME_COUNT))
print(' w x h : {} x {}'.format(w,h))
print('frame_cnt1:', frame_cnt1)
print('frame_cnt2:', frame_cnt2)

fps = cap1.get(cv2.CAP_PROP_FPS)
delay = int(200 / fps)
 
#create the file
fourcc = cv2.VideoWriter_fourcc(*'DIVX') # DivX MPEG-4 codec
out = cv2.VideoWriter('output.avi', fourcc, fps, (w , h))


# 합성 여부 Flag
do_composit = False

# play videos
while True:
    ret1, frame1 = cap1.read()

    if not ret1:
        break
    
    # do_composit 플래그가 True일 때에만 합성
    if do_composit:
        ret2, frame2 = cap2.read()

        if not ret2:
            break

        # HSV 색 공간에서 검출할 색 영역을 지정하고 영상 1에서 존재하는 그 색만을 검출하여 합성
        hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (50, 150, 0), (70, 255, 255))
        cv2.copyTo(frame2, mask, frame1)

    
    out.write(frame1)

    cv2.imshow('frame', frame1)
    key = cv2.waitKey(delay)

    # 스페이스바를 누르면 do_composit 플래그를 변경하여 적용할지 말지를 결정
    if key == ord(' '):
        do_composit = not do_composit
    elif key == 27: # ESC로 종료
        break

cap1.release()
cap2.release()
cv2.destroyAllWindows()
