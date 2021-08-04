import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
mpFace = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
faces = mpFace.FaceDetection(0.75)

ptime = 0
ctime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faces.process(imgRGB)

    if results.detections:
        for id, box in enumerate(results.detections):
            # print(box.score)
            # print(box.location_data.relative_bounding_box)
            bboxC = box.location_data.relative_bounding_box
            h, w, c = img.shape
            bbox = int(bboxC.xmin * w), int(bboxC.ymin * h),\
                    int(bboxC.width * w), int(bboxC.height * h)
            cv2.rectang(img, bbox, (255, 0, 255), 2)
            #mp_drawing.draw_detection(
            #    img, box)
            cv2.putText(img, f'{int(box.score[0] * 100)}%', (bbox[0], bbox[1] - 20),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(img, str(int(fps)), (18, 78),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

    if 0xFF == ord('q'):
        break
