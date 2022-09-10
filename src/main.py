import cv2
import numpy as np
import utils
import board
from adafruit_motorkit import MotorKit
from adafruit_servokit import ServoKit
import time
import digitalio

from board import SCL, SDA
import busio
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont




if __name__ == '__main__':

    servo = ServoKit(channels=16)
    dcMotor = MotorKit(i2c=board.I2C())


    i2c = busio.I2C(SCL, SDA)
    ina2 = INA219(i2c,addr=0x41)

    disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
    disp.fill(0)
    disp.show()
    width = disp.width
    height = disp.height
    image = Image.new("1", (width, height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    padding = -2
    top = padding
    bottom = height - padding
    x = 0
    font = ImageFont.truetype('/usr/share/fonts/truetype/ttf-bitstream-vera/Vera.ttf', 12)



    print("System Ready!")

    lowerWall = np.array([0, 0, 87])
    upperWall = np.array([179, 255, 255])

    lowerBlue = np.array([92, 95, 82])
    upperBlue = np.array([123, 174, 139])

    lowerOrange = np.array([0, 73, 87])
    upperOrange = np.array([20, 204, 166])

    cap = cv2.VideoCapture("/dev/video0")

    zero = 0.2
    kp = 0.55
    y = 479
    speed = 0.6
    lines = 0
    turnRight = True

    while True:

        success, img = cap.read()

        blueThres = utils.thresholding(img, lowerBlue, upperBlue)
        orangeThres = utils.thresholding(img, lowerOrange, upperOrange)
        blueDot = blueThres[y:y+10, 320:330]
        orangeDot = orangeThres[y:y+10, 320:330]
        print("y=", y, " blue=", np.sum(blueDot), " orange=", np.sum(orangeDot))
        if np.sum(blueDot) > 0:
           print("GO LEFT!")
           turnRight = False
           break
        if np.sum(orangeDot) > 0:
           print("GO RIGHT!")
           break

        y = y - 10
        if y < 200:
           print("***NOT FOUND***")
           break
        cv2.waitKey(1)

    if turnRight == True:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((x, top + 0), "RIGHT" , font=font, fill=255)
        disp.image(image)
        disp.show()
    else:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((x, top + 0), "LEFT" , font=font, fill=255)
        disp.image(image)
        disp.show()

    while True:
        button = digitalio.DigitalInOut(board.D24)
        button.direction = digitalio.Direction.INPUT
        if button.value == False:
            break
    while True:
        button = digitalio.DigitalInOut(board.D24)
        button.direction = digitalio.Direction.INPUT
        if button.value == True:
            break


    start_time = time.perf_counter()
    while True:
       servo.continuous_servo[0].throttle = zero
       success, img = cap.read()
       dcMotor.motor3.throttle = speed

       imgThres = utils.thresholding(img, lowerWall, upperWall)
       orangeThres = utils.thresholding(img, lowerOrange, upperOrange)
       blueThres = utils.thresholding(img, lowerBlue, upperBlue)

       if turnRight == True:
          wall = imgThres[260:320, 0:260]
          dotImage = orangeThres[420:430, 320:330]
       else:
          wall = imgThres[260:320, 340:639]
          dotImage = blueThres[420:430, 320:330]

       if np.sum(dotImage) > 100 and time.perf_counter() - start_time > 0.2:
          lines = lines + 1
          print("line= ", lines, np.sum(dotImage))
          start_time = time.perf_counter()


       if np.sum(wall)/3978000 < 0.95:
          break






    start_time = time.perf_counter()
    while True:
        button = digitalio.DigitalInOut(board.D24)
        button.direction = digitalio.Direction.INPUT
        if button.value == False or lines == 12:
            break

        success, img = cap.read()
        dcMotor.motor3.throttle = speed

        imgThres = utils.thresholding(img, lowerWall, upperWall)
        orangeThres = utils.thresholding(img, lowerOrange, upperOrange)
        blueThres = utils.thresholding(img, lowerBlue, upperBlue)

        if turnRight == True:
           wall = imgThres[260:320, 0:260]
           dotImage = orangeThres[420:430, 320:330]
        else:
           wall = imgThres[260:320, 340:639]
           dotImage = blueThres[420:430, 320:330]



        if np.sum(dotImage) > 1000 and time.perf_counter() - start_time > 0.2:
           lines = lines + 1
           print("line= ", lines, np.sum(dotImage))
           start_time = time.perf_counter()

        if turnRight == True:
           turn = 0.7 - np.sum(wall)/3978000
        else:
           turn = -0.7 + np.sum(wall)/3978000

        servo.continuous_servo[0].throttle = zero + kp * (turn)



        cv2.waitKey(1)


    print("TIME!!")
    start_time = time.perf_counter()
    while time.perf_counter() - start_time < 4:
        success, img = cap.read()
        dcMotor.motor3.throttle = speed

        imgThres = utils.thresholding(img, lowerWall, upperWall)

        if turnRight == True:
           wall = imgThres[260:320, 0:260]
        else:
           wall = imgThres[260:320, 340:639]

        if turnRight == True:
           turn = 0.7 - np.sum(wall)/3978000
        else:
           turn = -0.7 + np.sum(wall)/3978000

        servo.continuous_servo[0].throttle = zero + kp * (turn)

    dcMotor.motor3.throttle = 0

