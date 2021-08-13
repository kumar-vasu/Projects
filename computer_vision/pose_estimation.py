import cv2
import mediapipe as mp
import time

mppose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mppose.Pose()


cap = cv2.VideoCapture(0)
ctime = 0
ptime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            img, results.pose_landmarks, mppose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cv = int(lm.x * w), int(lm.y * h)

    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(img, str(int(fps)), (18, 78),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
