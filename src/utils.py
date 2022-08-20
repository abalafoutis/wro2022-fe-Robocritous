import cv2
import numpy as np

def thresholding(img, lower, upper):
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # lowerWhite = np.array([0,0,0])
    # upperWhite = np.array([179, 255, 255])
    maskWhite = cv2.inRange(imgHsv, lower, upper)

    return maskWhite

def warpImg(img, points, w, h, inv=False):
    pts1 = np.float32(points)
    pts2 = np.float32([[0,0], [w,0], [0,h], [w,h]])
    if inv:
        matrix = cv2.getPerspectiveTransform(pts2, pts1)
    else:
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv2.warpPerspective(img, matrix, (w, h))
    return imgWarp


def empty(a):
   pass

def initializeTrackBars(wT=320, hT=240):
    cv2.namedWindow("TrackBars")
    cv2.resizeWindow("TrackBars", wT, hT)
    cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
    cv2.createTrackbar("Hue Max", "TrackBars", 0, 179, empty)
    cv2.createTrackbar("Sat Min", "TrackBars", 0, 255, empty)
    cv2.createTrackbar("Sat Max", "TrackBars", 0, 255, empty)
    cv2.createTrackbar("Val Min", "TrackBars", 0, 255, empty)
    cv2.createTrackbar("Val Max", "TrackBars", 0, 255, empty)

def valTrackBars():
    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    print(h_min,h_max,s_min,s_max,v_min,v_max)
    lower = [h_min, s_min, v_min]
    upper = [h_max, s_max, v_max]
    return np.array(lower), np.array(upper)

def initializeTrackBars2(initialTrackBarVals, wT=480, hT=240):
    cv2.namedWindow("TrackBars")
    cv2.resizeWindow("TrackBars", wT, hT)
    cv2.createTrackbar("Width Top", "TrackBars", initialTrackBarVals[0], wT, empty)
    cv2.createTrackbar("Height Top", "TrackBars", initialTrackBarVals[1], hT, empty)
    cv2.createTrackbar("Width Bottom", "TrackBars", initialTrackBarVals[2], wT, empty)
    cv2.createTrackbar("Height Bottom", "TrackBars", initialTrackBarVals[3], hT, empty)

def valTrackBars2(wT=480, hT=240):
    widthTop = cv2.getTrackbarPos("Width Top", "TrackBars")
    heightTop = cv2.getTrackbarPos("Height Top", "TrackBars")
    widthBottom = cv2.getTrackbarPos("Width Bottom", "TrackBars")
    heightBottom = cv2.getTrackbarPos("Height Bottom", "TrackBars")
    print(widthTop, heightTop, widthBottom, heightBottom)
    points = np.float32([(widthTop, heightTop), (wT - widthTop, heightTop), (widthBottom, heightBottom), (wT - widthBottom, heightBottom)])
    return points

def drawPoints(img, points):
    for x in range(4):
        cv2.circle(img, (int(points[x][0]), int(points[x][1])), 15, (0,0,255), cv2.FILLED)
    return img

def getHistogram(img, minPer=0.1, display=False, region=1):
    if region == 1:
        histValues = np.sum(img, axis=0)
    else:
        histValues = np.sum(img[img.shape[0] // region:, :], axis=0)

    maxValue = np.max(histValues)
    minValue = minPer * maxValue
    indexArray = np.where(histValues >= minValue)
    basePoint = int(np.average(indexArray))

    if display:
        imgHist = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        for x, intensity in enumerate(histValues):
            cv2.line(imgHist, (x, img.shape[0]), (x, img.shape[0] - int(intensity)//255//region), (255,0,255), 1)
            cv2.circle(imgHist, (basePoint, img.shape[0]), 20, (0,255,255), cv2.FILLED)
        return basePoint, imgHist
    return basePoint

def line_point(image):
    image = image // 255
    image = 1 - image
    image = image * 255

    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    maxArea = 0
    i = 0
    max_i = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > maxArea:
            maxArea = area
            max_i = i
        i += 1


    try:
        kpCnt = len(contours[max_i])
    except:
        return 0

    if maxArea < 10:
        return 0

    x = 0
    y = 0

    for kp in contours[max_i]:
        x = x + kp[0][0]
        y = y + kp[0][1]
    # cv2.circle(img2, (np.uint8(np.ceil(x / kpCnt)), np.uint8(np.ceil(y / kpCnt))), 1, (0, 0, 255), 3)

    return np.uint8(np.ceil(y / kpCnt))