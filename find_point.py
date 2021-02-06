import cv2
import numpy as np


cap = cv2.VideoCapture(1)

while(1):
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([0, 20, 100])
    upper_yellow = np.array([25, 255, 255])

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    fontColor = (255, 255, 255)
    lineType = 2


    kernel = np.ones((5,5), np.uint8)
    erosion = cv2.erode(mask, kernel, iterations=1)
    dialation = cv2.dilate(erosion, kernel, iterations=1)

    contours, _ = cv2.findContours(dialation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        area = cv2.contourArea(contour)
        #print(area)

        if area > 800:
            cv2.drawContours(frame, contour, -1, (0, 255, 0), 3)

            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(frame, center, radius, (255, 0, 0), 2)

            cv2.putText(frame, 
                str(center),
                center,
                font,
                fontScale,
                fontColor,
                lineType)
    
    cv2.imshow('Original', frame)
    #cv2.imshow('Mask', mask)
    #cv2.imshow('Erosion', erosion)
    #cv2.imshow('Dilation', dialation)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()