import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
mpFacemesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
facemesh = mpFacemesh.FaceMesh(max_num_faces=2)
drawSpecs = mpDraw.DrawingSpec(thickness=2, circle_radius=2)

ptime = 0
ctime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = facemesh.process(imgRGB)

    if results.multi_face_landmarks:
        for facelms in results.multi_face_landmarks:
            for id, lm in enumerate(facelms.landmark):
                h, w, c = img.shape
                cx, cv = int(lm.x * w), int(lm.y * h)
            mp_drawing.draw_landmarks(
                img, facelms, mpFacemesh.FACE_CONNECTIONS, drawSpecs, drawSpecs)

    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(img, str(int(fps)), (18, 78),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

    if 0xFF == ord('q'):
        break
