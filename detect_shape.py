import math
import cv2
import sys

def setLabel(img, pts, label):
    (x, y, w, h) = cv2.boundingRect(pts)
    # cv2.boundingRect function은 contour에 외접하고 똑바로 세워진 직사각형의 
    # 좌상단 꼭지점 좌표 (x, y) 와 가로 세로 폭을 리턴하게 된다. 이 좌표를 기반으로 
    # 인식한 사물 겉 테두리에 사각형을 그리게 됨

    pt1 = (x, y)
    pt2 = (x + w, y + h)
    cv2.rectangle(img, pt1, pt2, (0, 0, 255), 1)
    cv2.putText(img, label, pt1, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))


def main():
    img = cv2.imread('polygon.bmp', cv2.IMREAD_COLOR)

    if img is None:
        print('Nope!')
        sys.exit()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_bin  = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    contours, _ = cv2.findContours( img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # ndarrray 값으로 반환되는 contours 값을 사용하여

    # pts가 객체 하나하나의 외각선 엔디? array를 같는 형태로 반환 가능

    for pts in contours:
        if cv2.contourArea(pts) < 400 : # 너무 작으면 무시, 가로 세로 20 pixel 미만은 무시, 노이즈 값 제거
            continue

        approx = cv2.approxPolyDP(pts, cv2.arcLength(pts, True)*0.02, True )

        vtc = len(approx)

        if vtc == 3:
            setLabel(img, pts, 'TRI')
        elif vtc == 4:
            setLabel(img, pts, 'RECT')
        elif vtc == 5:
            setLabel(img, pts, 'PENTA')
        elif vtc == 6:
            setLabel(img, pts, 'Hepta')
        elif vtc == 10:
            setLabel(img, pts, 'Star')
        else:
            length = cv2.arcLength(pts, True)
            area = cv2.contourArea(pts)
            ratio = 4. * math.pi * area / (length * length)

            if ratio > 0.7:
                setLabel(img, pts, 'CIR')
    
    cv2.imshow('img', img)
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()






