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

    lowerWall = np.array([0, 0, 87])
    upperWall = np.array([179, 255, 255])

    lowerBlue = np.array([92, 95, 82])
    upperBlue = np.array([123, 174, 139])

    lowerOrange = np.array([0, 73, 87])
    upperOrange = np.array([20, 204, 166])

    cap = cv2.VideoCapture("/dev/video0")
    kp = 0.5

    count = 0
    y = 450
    while True:

        success, img = cap.read()

        blueThres = utils.thresholding(img, lowerBlue, upperBlue)
        orangeThres = utils.thresholding(img, lowerOrange, upperOrange)
        blueDot = blueThres[y:y+10, 320:330]
        orangeDot = orangeThres[y:y+10, 320:330]
        #print("y=", y, " blue=", np.sum(blueDot), " orange=", np.sum(orangeDot))
        if np.sum(blueDot) > 50:
           print("GO LEFT!")
           break
        if np.sum(orangeDot) > 50:
           print("GO RIGHT!")
           break

        y = y - 10
        if y < 0:
           print("ERROR y negative")
        cv2.waitKey(1)

    lines = 0
    start_time = time.perf_counter()
    while True:
        button = digitalio.DigitalInOut(board.D24)
        button.direction = digitalio.Direction.INPUT
        if button.value == False or lines == 5:
            break

        success, img = cap.read()
        dcMotor.motor3.throttle = 0.6

        imgThres = utils.thresholding(img, lowerWall, upperWall)
        orangeThres = utils.thresholding(img, lowerOrange, upperOrange)

        leftImage = imgThres[260:320, 0:260]
        dotImage = orangeThres[320:330, 320:330]

        if np.sum(dotImage) > 100 and time.perf_counter() - start_time > 0.2:
           lines = lines + 1
           print(lines)
           start_time = time.perf_counter()

        left = 0.7 - np.sum(leftImage)/3978000

        servo.continuous_servo[0].throttle = zero + kp * (left)



        cv2.waitKey(1)

    dcMotor.motor3.throttle = 0
    print("lines= ", lines)

