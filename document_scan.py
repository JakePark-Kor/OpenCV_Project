import sys
import numpy as np
import cv2

#ROI
def drawROI(img, corners):
    cpy = img.copy()

    c1 = (128, 128, 255)
    c2 = (50, 50, 255)

    for pt in corners:
        cv2.circle(cpy, tuple(pt.astype(int)), 25, c1, -1, cv2.LINE_AA)

    cv2.line(cpy, tuple(corners[0].astype(int)), tuple(corners[1].astype(int)), c2, 2, cv2.LINE_AA)
    cv2.line(cpy, tuple(corners[1].astype(int)), tuple(corners[2].astype(int)), c2, 2, cv2.LINE_AA)
    cv2.line(cpy, tuple(corners[2].astype(int)), tuple(corners[3].astype(int)), c2, 2, cv2.LINE_AA)
    cv2.line(cpy, tuple(corners[3].astype(int)), tuple(corners[0].astype(int)), c2, 2, cv2.LINE_AA)

    disp = cv2.addWeighted(img, 0.3, cpy, 0.7, 0)

    return disp

# Mouse Action
def onMouse(event, x, y, flags, param):
    global srcQuad, dragSrc, ptOld, src

# When a user clicks left button

    if event == cv2.EVENT_LBUTTONDOWN:
        for i in range(4):
            if cv2.norm(srcQuad[i] - (x, y)) < 25:
                dragSrc[i] = True
                ptOld = (x, y)
                break
                
# When a user releases left button
    if event == cv2.EVENT_LBUTTONUP:
        for i in range(4):
            dragSrc[i] = False
         
# When a user moves a mouse while clicking
    if event == cv2.EVENT_MOUSEMOVE:
        for i in range(4):
            if dragSrc[i]:
                dx = x - ptOld[0]
                dy = y - ptOld[1]
                # displacement

                srcQuad[i] += (dx, dy)

                cpy = drawROI(src, srcQuad)
                cv2.imshow('img', cpy)
                ptOld = (x, y)
                break


# input image .jpg, .bmp, etc
src = cv2.imread('.jpg')

if src is None:
    print('Image open failed!')
    sys.exit()

# the size of input & output 
h, w = src.shape[:2] # height, width 
dw = 500
dh = round(dw * 297 / 210)  # A4 size: 210x297cm

# Coords for corner points, check whether dragging process happened or not 
srcQuad = np.array([[30, 30], [30, h-30], [w-30, h-30], [w-30, 30]], np.float32)
dstQuad = np.array([[0, 0], [0, dh-1], [dw-1, dh-1], [dw-1, 0]], np.float32)
dragSrc = [False, False, False, False]

# corner points, drawing rectangle
disp = drawROI(src, srcQuad)

cv2.imshow('img', disp)
cv2.setMouseCallback('img', onMouse)

while True:
    key = cv2.waitKey()
    if key == 13:  # ENTER Key
        break
    elif key == 27:  # ESC Key
        cv2.destroyWindow('img')
        sys.exit()

# Perspective Transform
pers = cv2.getPerspectiveTransform(srcQuad, dstQuad)
dst = cv2.warpPerspective(src, pers, (dw, dh), flags=cv2.INTER_CUBIC)

# Output resultant image
cv2.imshow('dst', dst)
cv2.waitKey()
cv2.destroyAllWindows()
