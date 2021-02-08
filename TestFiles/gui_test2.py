import numpy as np
import cv2
import tkinter as tk
import PIL.Image, PIL.ImageTk
from tkSliderWidget import Slider

MIN_AREA = 800

isColorBtn = False
isThresholdBth = True


threshold_min = np.array([0, 0 ,0 ])
threshold_max = np.array([255, 255, 255])


#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("Galactic Search Calibration")
window.config(background="#FFFFFF")

#Graphics window
imageFrame = tk.Frame(window, width=600, height=500)
imageFrame.grid(row=0, column=0, padx=10, pady=2)
imageFrame2 = tk.Frame(window, width=600, height=500)
imageFrame2.grid(row=0, column=1, padx=10, pady=2)

#Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)
l2 = tk.Label(imageFrame2)
l2.grid(row=0, column=1)
cap = cv2.VideoCapture(0)


def show_frame():
    #_, frame = cap.read()
    #frame = cv2.flip(frame, 1)
    #cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)



    _, frame = cap.read() #reads the current fame of the video
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #converts the current frame into a HSV Hue, Saturation, Value type


    #lower_yellow = np.array([0, 20, 100]) #Sets lower bound for threshold filtering may need to adjust depending on lighting
    #upper_yellow = np.array([25, 255, 255]) #Sets upper bound for threshold filtering

    mask = cv2.inRange(hsv, threshold_min, threshold_max) #removes out anything in the frame outside of the threshold bounds
    res = cv2.bitwise_and(frame, frame, mask=mask)

    #set up font to add text to video
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    fontColor = (255, 255, 255)
    lineType = 2

    #performs some steps to clean out noise and false positives
    kernel = np.ones((5,5), np.uint8)
    erosion = cv2.erode(mask, kernel, iterations=1)
    dialation = cv2.dilate(erosion, kernel, iterations=1)

    #finds array of countours that meet the threshold filtering critera
    contours, _ = cv2.findContours(dialation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    #print(isColorBtn)


    if isColorBtn:
        #cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        #current_img = cv2image
        current_img = frame
        #print('color')
    else:
        current_img = dialation
        #print('not_color')

    #loops through the contours
    for contour in contours:
        area = cv2.contourArea(contour) #determines the area of the contour
        #print(area)

        if area > MIN_AREA: #filters out contours smaller than the min area
            cv2.drawContours(current_img, contour, -1, (0, 255, 0), 3) #draws the true contour on the video

            #finds the minimum bounding circle of the contour also determines the circle center point and radius
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(current_img, center, radius, (255, 0, 0), 2)

            #adds the coordinate points of the center of the contour on the video
            cv2.putText(current_img, 
                str(center),
                center,
                font,
                fontScale,
                fontColor,
                lineType)
    
    #shows the image of the video
    #cv2.imshow('Original', frame)
    #cv2.imshow('Mask', mask)  #shows the masked image uncomment to see the threshold filtering
    #cv2.imshow('Erosion', erosion) #shows the image after erosion step
    #cv2.imshow('Dilation', dialation) #shows the image after dialation step













    #img = PIL.Image.fromarray(frame)
    img = PIL.Image.fromarray(current_img)
    imgtk = PIL.ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)


#    l2.imgtk = imgtk
#    l2.configure(image=imgtk)
#    l2.after(10, show_frame) 

    hue_min, hue_max = hueSlider.getValues()
    sat_min, sat_max = satSlider.getValues()
    val_min, val_max = valSlider.getValues()
    threshold_min[0] = int(hue_min)
    threshold_max[0] = int(hue_max)
    threshold_min[1] = int(sat_min)
    threshold_max[1] = int(sat_max)
    threshold_min[2] = int(val_min)
    threshold_max[2] = int(val_max)


def colorBtn():
    print('color button')
    global isColorBtn, isThresholdBth
    isColorBtn = True
    isThresholdBth = False

def thresholdBtn():
    print('thrsh btn')
    global isColorBtn, isThresholdBth
    isThresholdBth = True
    isColorBtn = False
    


colorImageBtn = tk.Button(window, text = "Color", command=colorBtn)
colorImageBtn.grid(row = 1, column = 0)

thresholdImageBtn = tk.Button(window, text = "Threshold", command=thresholdBtn)
thresholdImageBtn.grid(row = 1, column = 1)


hueSlider = Slider(window, width = 400, height = 60, min_val = 0, max_val = 255, init_lis = [0,255], show_value = True)
hueSlider.grid(row = 2, column=0)

satSlider = Slider(window, width = 400, height = 60, min_val = 0, max_val = 255, init_lis = [0,255], show_value = True)
satSlider.grid(row = 3, column=0)

valSlider = Slider(window, width = 400, height = 60, min_val = 0, max_val = 255, init_lis = [0,255], show_value = True)
valSlider.grid(row = 4, column=0)


show_frame()  #Display 2
window.mainloop()  #Starts GUI