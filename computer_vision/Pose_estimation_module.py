import cv2
import mediapipe as mp
import time


class pose_detector():
    def __init__(self, mode=False, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mppose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mppose.Pose(
            self.mode, self.upBody, self.smooth, self.detectionCon, self.trackCon)

    def findpose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks:
            if draw:
                self.mp_drawing.draw_landmarks(img,
                                               self.results.pose_landmarks,
                                               self.mppose.POSE_CONNECTIONS)
        return img

    def findposition(self, img, draw=True):
        lm_list = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cv = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cv])
                if draw:
                    cv2.circle(img, (cx, cv), 15, (255, 0, 255), cv2.FILLED)
        return lm_list

# dummy code for use


def main():
    ptime = 0
    ctime = 0
    cap = cv2.VideoCapture(0)
    detector = pose_detector()

    while True:
        success, img = cap.read()
        img = detector.findpose(img)
        lm_list = detector.findposition(img)
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
