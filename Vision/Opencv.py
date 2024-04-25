import cv2 as cv
import numpy as np
import time

video_capture = cv.VideoCapture(2)
prevCircle = None
dist = lambda x1,y1,x2,y2: (x1-x2)**2 + (y1-y2)**2
prev_frame_time = 0
new_frame_time = 0

while True:
    ret, frame = video_capture.read()
    if not ret: break

    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurFrame = cv.GaussianBlur(grayFrame, (7, 7), 0)

    font = cv.FONT_HERSHEY_SIMPLEX
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time

    fps = int(fps)
    fps = str(fps)

    cv.putText(frame, fps, (7, 70), font, 3, 3, cv.LINE_AA)

    circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1.4, 110,
                              param1=160,param2=50,minRadius=10, maxRadius=100)
    # param1 = sensibility paramqqqq2 = accurrancy
    if circles is not None:
        circles = np.uint16(np.around(circles))
        chosen = None
        for i in circles[0, :]:
            if chosen is None: chosen = i
            if prevCircle is not None:
                if dist(chosen[0],chosen[1],prevCircle[0],prevCircle[1] <= dist(i[0],i[1],prevCircle[0],prevCircle[1])):
                   chosen = i

        print(fps)
        cv.circle(frame, (chosen[0], chosen[1]), 1, (0,180,180), 3)
        cv.circle(frame,(chosen[0], chosen[1]), chosen[2], (255,0,255),3)
        prevCircle = chosen 

    
    
    #cv.imshow('circles', blurFrame)
    cv.imshow('circles', frame)

    if cv.waitKey(1) & 0xFF == ord('q'): break

video_capture.release()

cv.destroyAllWindows()