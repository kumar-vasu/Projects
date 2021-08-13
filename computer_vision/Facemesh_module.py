import cv2
import mediapipe as mp
import time


class Facemesh():
    def __init__(self, mode=False, maxFaces=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxFaces = maxFaces
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpFacemesh = mp.solutions.face_mesh
        self.facemesh = mpFacemesh.FaceMesh(self.mode, self.maxFaces,
                                            self.detectionCon, self.trackCon)
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawSpecs = mpDraw.DrawingSpec(thickness=2, circle_radius=2)

    def genmesh(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.facemesh.process(imgRGB)

        if self.results.multi_face_landmarks:
            for facelms in self.results.multi_face_landmarks:
                if draw:
                    self.mp_drawing.draw_landmarks(img,
                                                   facelms, self.mpFacemesh.FACE_CONNECTIONS, self.drawSpecs, self.drawSpecs)
        return img

    def findposition(self, img, faceno=0, draw=True):
        lm_list = []
        if self.results.multi_hand_landmarks:
            myface = self.results.multi_hand_landmarks[faceno]
            for id, lm in enumerate(myface.landmark):
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
    detector = Facemesh()

    while True:
        success, img = cap.read()
        img = detector.genmesh(img)
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
