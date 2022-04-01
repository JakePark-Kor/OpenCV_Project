import sys
import numpy as np
import cv2


# 두 개의 동영상을 열어서 video1, video2로 지정
video1 = cv2.VideoCapture('video1.mp4')
video2 = cv2.VideoCapture('video2.mp4')

if not cap1.isOpened() or not cap2.isOpened():
    print("Video FAILED to load")
    sys.exit()

# Assume that the frames of 2 videos are same 
frame_cnt1 = round(video1.get(cv2.CAP_PROP_FRAME_COUNT))
frame_cnt2 = round(video2.get(cv2.CAP_PROP_FRAME_COUNT))
fps = video1.get(cv2.CAP_PROP_FPS)
effect_frames = int(fps * 2) # The merge is for first 2 sec

print('frame_cnt1:', frame_cnt1)
print('frame_cnt2:', frame_cnt2)
print('FPS:', fps)

delay =int(100 /fps)

w = round(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
h = round(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
 
# Create the file for the result 
result = cv2.VideoWriter('output.avi', fourcc, fps, (w, h))

# Copy video1

'''
while True:
    ret1, frame1 = video1.read()

    if not ret1:
        break
    
    out.write(frame1)

    cv2.imshow('frame', frame1)
    cv2.waitKey(delay)

while True:
    ret2, frame2 = cap2.read()

    if not ret2:
        break

    out.write(frame2)

    cv2.imshow('frame', frame2)
    cv2.waitKey(delay)
    
'''
for i in range(frame_cnt1 - effect_frames):
    ret1, frame1 = video.read()

    if not ret1:
        break

    out.write(frame1)

    cv2.imshow('frame', frame1)
    cv2.waitKey(delay)

for i in range(effect_frames):
    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()

# Merging the back of video1 and first 2 sec of video2 
    dx = int(w * i / effect_frames)

    # frame = np.zeros((h, w, 3), dtype = np.uint8)
    # frame[:, 0 : dx] = frame2[:, 0 : dx]
    # frame[:, dx:w] = frame1[:, dx: w]
    alpha = 1.0 - i/ effect_frames 
    frame = cv2.addWeighted(frame1, alpha, frame2, 1 - alpha, 0)
    result.write(frame)
    cv2.imshow('frame', frame)
    cv2.waitKey(delay)


# copy video2

for i in range(effect_frames, frame_cnt2):
    ret2, frame2 = video2.read()

    if not ret2:
        break

    out.write(frame2)

    cv2.imshow('frame', frame2)
    cv2.waitKey(delay)

video1.release()
video2.release()
result.release()
cv2.destroyAllWindows()
