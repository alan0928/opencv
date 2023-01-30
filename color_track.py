import cv2
import numpy as np

video = cv2.VideoCapture(0)

drawPoints = []
blue = [255, 0, 0]
green = [0, 255, 0]
data = [[76, 82, 146, 92, 199, 233, green], [107, 135, 136, 119, 209, 253, blue]]

def findPen(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    for i in range(2):
        lower = np.array(data[i][:3])
        upper = np.array(data[i][3:6])

        mask = cv2.inRange(hsv, lower, upper) 
        # result = cv2.bitwise_and(frame, frame, mask=mask)
        penx, peny = findContour(mask)
        # cv2.imshow('result', result)
        if peny != -1:
            drawPoints.append([penx, peny, data[i][6]])

def findContour(img): 
    contour, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = -1, -1, -1, -1
    for cnt in contour:
        cv2.drawContours(imgContour, cnt, -1, (0, 255, 0), 4)
        area = cv2.contourArea(cnt)
        if area > 500:
            peri = cv2.arcLength(cnt, True)
            ver = cv2.approxPolyDP(cnt, peri * 0.02, True)
            x, y, w, h = cv2.boundingRect(ver) 
    return x + w//2, y

def draw(drawpoints):
    for points in drawpoints:
        cv2.circle(imgContour, (points[0], points[1]), 10, points[2], cv2.FILLED)

while True:
    ret , frame = video.read()
    frame = cv2.resize(frame , (700 , 500))
    if ret:
        imgContour = frame.copy()
        # cv2.imshow('video' , frame)
        findPen(frame)
        draw(drawPoints)
        cv2.imshow('contour', imgContour)
    else:
        break
    if cv2.waitKey(10) == ord(' '):
        break