import cv2
import mediapipe as mp
import time


class face_detector():
    def __init__(self, minDetectionCon=0.5):
        self.minDetectionCon = minDetectionCon
        self.mpFace = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.faces = self.mpFace.FaceDetection(minDetectionCon)

    def findfaces(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faces.process(imgRGB)
        bboxes = []

        if self.results.detections:
            for id, box in enumerate(self.results.detections):
                # print(box.score)
                # print(box.location_data.relative_bounding_box)
                bboxC = box.location_data.relative_bounding_box
                h, w, c = img.shape
                bbox = int(bboxC.xmin * w), int(bboxC.ymin * h),\
                    int(bboxC.width * w), int(bboxC.height * h)
                bboxes.append([bbox, box.score])
                if draw:
                    img = self.fancyDraw(img, bbox)
                    # mp_drawing.draw_detection(
                    #    img, box)
                    cv2.putText(img, f'{int(box.score[0] * 100)}%', (bbox[0], bbox[1] - 20),
                                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        return img, bboxes

    def fancyDraw(self, img, bbox, l=30, t=5):
        x, y, w, h = bbox
        x1, y1 = x + w, y + h
        cv2.rectangle(img, bbox, (255, 0, 255), 1)

        # top left
        cv2.line(img, (x, y), (x + 30, y), (255, 0, 255), t)
        cv2.line(img, (x, y), (x, y + 30), (255, 0, 255), t)
        # top right
        cv2.line(img, (x1, y), (x1 - 30, y), (255, 0, 255), t)
        cv2.line(img, (x1, y), (x1, y + 30), (255, 0, 255), t)
        # bottom left
        cv2.line(img, (x, y1), (x + 30, y1), (255, 0, 255), t)
        cv2.line(img, (x, y1), (x, y1 - 30), (255, 0, 255), t)
        # bottom left
        cv2.line(img, (x1, y1), (x1 - 30, y1), (255, 0, 255), t)
        cv2.line(img, (x1, y1), (x1, y1 - 30), (255, 0, 255), t)
        return img

# dummy code for use


def main():
    ptime = 0
    ctime = 0
    cap = cv2.VideoCapture(0)
    detector = face_detector()

    while True:
        success, img = cap.read()
        img, bboxes = detector.findfaces(img)
        if len(bboxes) != 0:
            print(bboxes)

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        cv2.putText(img, str(int(fps)), (18, 78),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
