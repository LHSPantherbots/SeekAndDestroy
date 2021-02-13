import cv2
import numpy as np
import sys
import time
from networktables import NetworkTables

import logging

logging.basicConfig(level=logging.DEBUG)


# Set up network tables to talk with robot

ip = "10.25.82.2"  # Robot IP Address 10.TE.AM.2
NetworkTables.initialize(server=ip)
sd = NetworkTables.getTable("SmartDashboard")
print(sd)
sd.putString("Test", "Gonzo was here")

# Starts video feed from webcam
cap = cv2.VideoCapture(1)


RAD = 50  # Radius of Error to find points
MIN_AREA = 250  # Minimum area of viable contour
path = "none"  # Output path determined


# navpoints - coordinates will have to be determined once camera is placed at a fixed posion
POINTS = [
    {"name": "C3", "coordinates": (695, 735), "radius": RAD, "isBall": False},
    {"name": "D5", "coordinates": (903, 456), "radius": RAD, "isBall": False},
    {"name": "A6", "coordinates": (270, 386), "radius": RAD, "isBall": False},
    {"name": "E6", "coordinates": (1067, 375), "radius": RAD, "isBall": False},
    {"name": "B7", "coordinates": (469, 321), "radius": RAD, "isBall": False},
    {"name": "C9", "coordinates": (643, 228), "radius": RAD, "isBall": False},
    {"name": "B3", "coordinates": (363, 755), "radius": RAD, "isBall": False},
    {"name": "D6", "coordinates": (867, 377), "radius": RAD, "isBall": False},
    {"name": "B8", "coordinates": (486, 273), "radius": RAD, "isBall": False},
    {"name": "D10", "coordinates": (770, 196), "radius": RAD, "isBall": False},
]


sd.putString("Path", path)
print(path)

# starts vidio processing loop to exit hit the esc key
while 1:
    _, frame = cap.read()  # reads the current fame of the video
    hsv = cv2.cvtColor(
        frame, cv2.COLOR_BGR2HSV
    )  # converts the current frame into a HSV Hue, Saturation, Value type

    lower_yellow = np.array([20, 102, 194])  # Sets lower bound for threshold filtering
    upper_yellow = np.array([36, 255, 255])  # Sets upper bound for threshold filtering

    mask = cv2.inRange(
        hsv, lower_yellow, upper_yellow
    )  # removes out anything in the frame outside of the threshold bounds
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # set up font to add text to video
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    fontColor = (255, 0, 255)
    lineType = 2

    # performs some steps to clean out noise and false positives
    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(mask, kernel, iterations=1)
    dialation = cv2.dilate(erosion, kernel, iterations=1)

    # finds array of countours that meet the threshold filtering critera
    contours, _ = cv2.findContours(dialation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # loops through each of the nav points to determine if a viable contour in the near vicinity of the point
    for point in POINTS:

        # loops through the contours
        for contour in contours:

            area = cv2.contourArea(contour)  # determines area of the contour

            if area > MIN_AREA:  # filters out contours smaller than the min area
                cv2.drawContours(
                    frame, contour, -1, (0, 255, 0), 3
                )  # draws the true contour on the video

                # finds the minimum bounding circle of the contour also determines the circle center point and radius
                (x, y), radius = cv2.minEnclosingCircle(contour)
                center = (int(x), int(y))
                radius = int(radius)
                cv2.circle(
                    frame, center, radius, (255, 0, 0), 2
                )  # draws the contour bounding circle onto the video

                # calculates the distance between each nav point and the current contour center point
                point1 = np.array(center)
                point2 = np.array(point["coordinates"])
                error = np.linalg.norm(point1 - point2)

                # determines if the distance from the contour center to the nav point is withing the specified radius
                if error < point["radius"]:

                    point[
                        "isBall"
                    ] = True  # if the ball is within the specified limits it states sets the point to have a ball

            # cv2.putText(frame,
            #     str(center),
            #     center,
            #     font,
            #     fontScale,
            #     fontColor,
            #     lineType)

    # determines if there is a ball on all of the proper points for a path if so will update the path network table value and display the path on the video
    if POINTS[0]["isBall"] and POINTS[1]["isBall"] and POINTS[2]["isBall"]:
        cv2.putText(
            frame, "Path A - Red", (10, 100), font, fontScale, fontColor, lineType
        )
        path = "Path A - Red"

    if POINTS[3]["isBall"] and POINTS[4]["isBall"] and POINTS[5]["isBall"]:
        cv2.putText(
            frame, "Path A - Blue", (10, 100), font, fontScale, fontColor, lineType
        )
        path = "Path A - Blue"

    if POINTS[6]["isBall"] and POINTS[1]["isBall"] and POINTS[4]["isBall"]:
        cv2.putText(
            frame, "Path B - Red", (10, 100), font, fontScale, fontColor, lineType
        )
        path = "Path B - Red"

    if POINTS[7]["isBall"] and POINTS[8]["isBall"] and POINTS[9]["isBall"]:
        cv2.putText(
            frame, "Path B - Blue", (10, 100), font, fontScale, fontColor, lineType
        )
        path = "Path B - Blue"

    print("Updating Path with ", path)
    sd.putString("Path", path)

    for point in POINTS:
        if point["isBall"]:
            cv2.circle(frame, point["coordinates"], point["radius"], (0, 255, 0), 2)
            cv2.putText(
                frame,
                point["name"],
                point["coordinates"],
                font,
                fontScale,
                fontColor,
                lineType,
            )
        else:
            cv2.circle(frame, point["coordinates"], point["radius"], (0, 0, 255), 2)
    
    cv2.imshow("Original", frame)
    # cv2.imshow('Mask', mask)
    # cv2.imshow('Erosion', erosion)
    # cv2.imshow('Dilation', dialation)

    # resets points to say there is no balls before the next loop
    for point in POINTS:
        point["isBall"] = False

    # resets path to say note befor next loop
    path = "none"

    # breaks loop if esc key is pressed
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()