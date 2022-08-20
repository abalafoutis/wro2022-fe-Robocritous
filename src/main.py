import cv2
import numpy as np
import utils
import board
from adafruit_motorkit import MotorKit
from adafruit_servokit import ServoKit
import time
import digitalio




if __name__ == '__main__':

    servo = ServoKit(channels=16)
    dcMotor = MotorKit(i2c=board.I2C())

    zero = 0.2
    print("System Ready!")

    lowerWall = np.array([0, 0, 120])
    upperWall = np.array([179, 255, 255])

    lowerBlue = np.array([0, 0, 100])
    upperBlue = np.array([179, 255, 255])

    lowerOrange = np.array([24, 0, 45])
    upperOrange = np.array([179, 255, 255])

    cap = cv2.VideoCapture("/dev/video0")
    kp = 0.5

    count = 0
    while count < 100:

        success, img = cap.read()

        blueThres = utils.thresholding(img, lowerBlue, upperBlue)
        orangeThres = utils.thresholding(img, lowerOrange, upperOrange)
        blueImage = blueThres[200:350, 220:440]
        orangeImage = orangeThres[200:350, 220:440]
        Y_orange = utils.line_point(orangeImage)
        Y_blue = utils.line_point(blueImage)
        print("Y_orange = ", Y_orange, " Y_blue = ", Y_blue)
        if Y_orange > Y_blue:
            print("GO RIGHT!")
        else:
            print("GO LEFT!")
        count += 1
        cv2.waitKey(1)


    while True:
        button = digitalio.DigitalInOut(board.D24)
        button.direction = digitalio.Direction.INPUT
        if button.value == False:
            break

        success, img = cap.read()
        dcMotor.motor3.throttle = 0.6

        imgThres = utils.thresholding(img, lowerWall, upperWall)

        leftImage = imgThres[260:320, 0:260]

        left = 0.7 - np.sum(leftImage)/3978000

        servo.continuous_servo[0].throttle = zero + kp * (left)


        cv2.waitKey(1)

    dcMotor.motor3.throttle = 0

