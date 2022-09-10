import cv2
import numpy as np
import utils

def getLaneCurve(img, lower, upper):
    imgThres = utils.thresholding(img, lower, upper)

    cv2.imshow('Thres', imgThres)
    return None

if __name__ == '__main__':
    cap = cv2.VideoCapture("/dev/video0")
    frameCounter = 0

    utils.initializeTrackBars()

    while True:
        frameCounter += 1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0

        success, img = cap.read()
        #img = cv2.resize(img, (480, 240))

        lower, upper = utils.valTrackBars()
        getLaneCurve(img, lower, upper)
        cv2.rectangle(img, (0, 260), (300, 320), (0, 0, 255), 2) # wall window
        cv2.rectangle(img, (320, 320), (330, 330), (255, 255, 0), 2)  # dot window

        cv2.imshow('vid', img)
        cv2.waitKey(1)