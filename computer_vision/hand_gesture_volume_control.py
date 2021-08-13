import cv2
import time
import Hand_Tracking_module as htm
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


ptime = 0
ctime = 0
cap = cv2.VideoCapture(0)
detector = htm.hand_detector(detectionCon=0.7)

###########################
# pycaw ###################

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(0, None)
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volbar = 400
volper = 0

##############################

while True:
    success, img = cap.read()
    img = detector.findhands(img)
    lm_list = detector.findposition(img, draw=False)
    if len(lm_list) != 0:
        x1, y1 = lm_list[4][1], lm_list[4][2]
        x2, y2 = lm_list[8][1], lm_list[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)
        # hand range 50 - 300
        # vol range -65 0
        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volbar = np.interp(length, [50, 300], [400, 150])
        volper = np.interp(length, [50, 300], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)
        print(vol)
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 1)
    cv2.rectangle(img, (50, int(volbar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volper)}%', (48, 450),
                cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(img, f'FPS: {int(fps)}', (18, 78),
                cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
