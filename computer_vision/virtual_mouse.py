import cv2
import Hand_Tracking_module as htm
import time
import numpy as np
import autopy

ptime = 0
ctime = 0
frameR = 100
smoothening = 7
plocX, plocY = 0, 0
clocX, clocY = 0, 0
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.hand_detector(maxHands=1)
wScr, hScr = autopy.screen.size()

while True:
    success, img = cap.read()
    img = detector.findhands(img)
    lm_list, bbox = detector.findposition(img, draw=False)

    if len(lm_list) != 0:
        # tip of index finger
        x1, y1 = lm_list[8][1:]

        # tip of middle finger
        x2, y2 = lm_list[12][1:]

        # checking which fingers are up
        fingers = detector.fingersup()

        # only index finger :moving mouse
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR,
                                              hCam - frameR), (255, 0, 255), 2)
        if fingers[1] == 1 and fingers[2] == 0:

            # convert coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR),
                           (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            # smoothen values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # move mouse
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # both index and middle fingers are up:clicking mode
        if fingers[1] == 1 and fingers[2] == 1:
            length, img, Lineinfo = detector.findDistance(8, 12, img)
            print(length)
            # find distACE BETWEEN FINGERS
            if length < 48:
                # click if distsnace is short
                cv2.circle(img, (Lineinfo[4], Lineinfo[5]),
                           15, (0, 255, 0), cv2.FILLED)
                # autopy.mouse.click()
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(img, str(int(fps)), (18, 78),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
