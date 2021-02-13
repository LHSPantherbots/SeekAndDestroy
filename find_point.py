import cv2
import numpy as np


MIN_AREA = 250 #minimum area of viable contour


#sets up camera to capture the video
cap = cv2.VideoCapture(1)

#loops the video feed until the esc key is pressed
while(1):

    _, frame = cap.read() #reads the current fame of the video
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #converts the current frame into a HSV Hue, Saturation, Value type

                # Hue, Saturation, V (brightness)
    lower_yellow = np.array([20, 102, 194]) #Sets lower bound for threshold filtering may need to adjust depending on lighting
    upper_yellow = np.array([36, 255, 255]) #Sets upper bound for threshold filtering

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow) #removes out anything in the frame outside of the threshold bounds
    res = cv2.bitwise_and(frame, frame, mask=mask)

    #set up font to add text to video
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    # B,G,R
    fontColor = (0, 0, 255)
    lineType = 2

    #performs some steps to clean out noise and false positives
    kernel = np.ones((5,5), np.uint8)
    erosion = cv2.erode(mask, kernel, iterations=1)
    dialation = cv2.dilate(erosion, kernel, iterations=1)

    #finds array of countours that meet the threshold filtering critera
    contours, _ = cv2.findContours(dialation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    #loops through the contours
    for contour in contours:
        area = cv2.contourArea(contour) #determines the area of the contour
        #print(area)

        if area > MIN_AREA: #filters out contours smaller than the min area
            cv2.drawContours(frame, contour, -1, (0, 255, 0), 3) #draws the true contour on the video

            #finds the minimum bounding circle of the contour also determines the circle center point and radius
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(frame, center, radius, (255, 0, 0), 2)

            #adds the coordinate points of the center of the contour on the video
            cv2.putText(frame, 
                str(center),
                center,
                font,
                fontScale,
                fontColor,
                lineType)
    
    #shows the image of the video
    cv2.imshow('Original', frame)
    #cv2.imshow('Mask', mask)  #shows the masked image uncomment to see the threshold filtering
    #cv2.imshow('Erosion', erosion) #shows the image after erosion step
    cv2.imshow('Dilation', dialation) #shows the image after dialation step

    #breaks loop if esc key is pressed
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()