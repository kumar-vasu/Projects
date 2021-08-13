import cv2
import mediapipe as mp
import time
import math
import numpy as np


class hand_detector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mpHands.Hands(
            self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.tipIds = [4, 8, 12, 16, 20]

    def findhands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:

                if draw:
                    self.mp_drawing.draw_landmarks(
                        img, handlms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findposition(self, img, handno=0, draw=True):
        self.lm_list = []
        xList = []
        vList = []
        bbox = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handno]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape
                cx, cv = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                vList.append(cv)
                self.lm_list.append([id, cx, cv])
                if draw:
                    cv2.circle(img, (cx, cv), 15, (255, 0, 255), cv2.FILLED)
            xmin, xmax = min(xList), max(xList)
            vmin, vmax = min(vList), max(vList)
            bbox = xmin, vmin, xmax, vmax

            if draw:
                cv2.rectangle(img, (xmin - 20, vmin - 20),
                              (xmax + 20, vmax + 20), (255, 0, 255), 2)

        return self.lm_list, bbox

    def fingersup(self):
        fingers = []
        if self.lm_list[self.tipIds[0]][1] > self.lm_list[self.tipIds[4]][1]:
            if self.lm_list[self.tipIds[0]][1] > self.lm_list[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            if self.lm_list[self.tipIds[0]][1] > self.lm_list[self.tipIds[0] - 1][1]:
                fingers.append(0)
            else:
                fingers.append(1)

        for id in range(1, 5):
            if self.lm_list[self.tipIds[id]][2] < self.lm_list[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=15, t=5):
        x1, y1 = self.lm_list[p1][1:]
        x2, y2 = self.lm_list[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)
        return length, img, [x1, y1, x2, y2, cx, cy]

# dummy code for use


def main():
    ptime = 0
    ctime = 0
    cap = cv2.VideoCapture(0)
    detector = hand_detector()

    while True:
        success, img = cap.read()
        img = detector.findhands(img)
        lm_list, bbox = detector.findposition(img)
        if len(lm_list) != 0:
            print(lm_list[4])

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        cv2.putText(img, str(int(fps)), (18, 78),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
