import os
import cv2
import numpy as np
import time
import Hand_Tracking_module as htm


brushthickness = 15

folderPath = "header"
mylist = os.listdir(folderPath)
overlaylist = []
for imPath in mylist:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlaylist.append(image)
header = overlaylist[0]
drawcolor = (51, 65, 227)

ptime = 0
ctime = 0
cap = cv2.VideoCapture(0)
cap.set(3, 1212)
cap.set(4, 720)
detector = htm.hand_detector(detectionCon=0.85)

xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    # import image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # find hand landmarks

    img = detector.findhands(img)
    lm_list = detector.findposition(img, draw=False)
    if len(lm_list) != 0:

        # tip of index finger
        x1, y1 = lm_list[8][1:]

        # tip of middle finger
        x2, y2 = lm_list[12][1:]

        # checking which fingers are up
        fingers = detector.fingersup()

        # if selection mode
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            print("selection")
            if y1 < 128:
                if 0 < x1 < 200:
                    header = overlaylist[0]
                    drawcolor = (51, 65, 227)
                elif 250 < x1 < 450:
                    header = overlaylist[1]
                    drawcolor = (5, 182, 243)
                elif 550 < x1 < 750:
                    header = overlaylist[2]
                    drawcolor = (80, 163, 50)
                elif 800 < x1 < 950:
                    header = overlaylist[3]
                    drawcolor = (236, 129, 64)
                elif 1050 < x1 < 1212:
                    header = overlaylist[4]
                    drawcolor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25),
                          drawcolor, cv2.FILLED)

        # if we have the drawing mode
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15,  drawcolor, cv2.FILLED)
            print("drawing")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawcolor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawcolor, 50)
                cv2.line(imgCanvas, (xp, yp), (x1, y1),
                         drawcolor, brushthickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawcolor, brushthickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1),
                         drawcolor, brushthickness)
            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 58, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # setting header
    img[0:128, 0:1212] = header

    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(img, str(int(fps)), (18, 78),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    print(len(img[0]))
    #img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow("Image", img)
    #cv2.imshow("canvas", imgCanvas)
    cv2.waitKey(1)
