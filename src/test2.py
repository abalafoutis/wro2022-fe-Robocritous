import cv2
import numpy as np
import utils


if __name__ == '__main__':

    lowerWall = np.array([0, 0, 87])
    upperWall = np.array([179, 255, 255])

    lowerBlue = np.array([92, 95, 82])
    upperBlue = np.array([123, 174, 139])

    lowerOrange = np.array([0, 73, 87])
    upperOrange = np.array([20, 204, 166])


    cap = cv2.VideoCapture("/dev/video0")

    while True:
        success, img = cap.read()


        wallThres = utils.thresholding(img, lowerWall, upperWall)
        blueThres = utils.thresholding(img, lowerBlue, upperBlue)
        orangeThres = utils.thresholding(img, lowerOrange, upperOrange)


        leftWall = wallThres[260:320, 0:260]
        dotImage = orangeThres[320:330, 320:330]

        # print("orage Y: " , utils.line_point(orangeImage))
        # print("blue Y: ", utils.line_point(blueImage))
        print(np.sum(dotImage))



        cv2.imshow('img', img)
        cv2.imshow('leftWall', leftWall)
        cv2.imshow('blue', blueImage)
        cv2.imshow('dotImage', dotImage)




        cv2.waitKey(1)

