import cv2 as cv
import mediapipe as mp 
import time

from mediapipe.python.solutions import hands
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
# Get default audio device using PyCAW
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# Get current volume 
# volume.SetMasterVolumeLevel(currentVolumeDb - 6.0, None)
# NOTE: -6.0 dB = half volume !

# cap = cv.VideoCapture("./videos/oyo.mp4")
cap = cv.VideoCapture(0,cv.CAP_DSHOW)

mpHands = mp.solutions.hands

hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
ptime =0
ctime = 0
center_thumbx = 0
center_thumby = 0
center_fingerx = 0
center_fingery = 0
while True:
     
     success,img = cap.read()
     imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
     results = hands.process(imgRGB)
     dic = results.multi_hand_landmarks
     if dic:
         for hand in dic:
             for id,lm in enumerate(hand.landmark):
                 h,w,c = img.shape
                 cx,cy = int(lm.x * w), int(lm.y*h)
                #  print(id,cx,cy)
                #  print(center_fingerx,center_fingery)
                 if id==4:
                     cv.circle(img,(cx,cy),25,(255,180,255),cv.FILLED)
                     center_thumbx = cx
                     center_thumby = cy
                    #  print(center_thumbx,center_thumby)
                 if id==8:
                     cv.circle(img,(cx,cy),25,(160,180,255),cv.FILLED)
                     center_fingerx = cx
                     center_fingery = cy
                    #  print(center_fingerx,center_fingery)



             mpDraw.draw_landmarks(img,hand,mpHands.HAND_CONNECTIONS)
     ctime = time.time()
     fps = 1/(ctime-ptime)
     ptime=ctime
     print(center_thumby,center_fingery)
     dist =center_thumby - center_fingery
     print(str(dist) + "yems this is distance")
     if dist>100:
         currentVolumeDb = volume.GetMasterVolumeLevel()
         print(str(currentVolumeDb) + "This is the volume ayooo")
         if currentVolumeDb !=0.0:
             volume.SetMasterVolumeLevel(currentVolumeDb + 0.5, None)
     else:
         currentVolumeDb = volume.GetMasterVolumeLevel()
         if currentVolumeDb !=-65.0:
             volume.SetMasterVolumeLevel(currentVolumeDb - 0.5, None)
     cv.putText(img,str(dist),(200,70),cv.FONT_HERSHEY_COMPLEX,3,(255,0,255),3)
     cv.putText(img,str(int(fps)),(10,70),cv.FONT_HERSHEY_COMPLEX,3,(255,0,255),3)
     cv.putText(img,str(currentVolumeDb),(10,450),cv.FONT_HERSHEY_COMPLEX,3,(255,0,255),3)
     if success == True:
            cv.imshow("results",img)
            # print(results.multi_hand_landmarks)
     else:
         break
     if cv.waitKey(1) & 0xFF == ord('q'):
         break

cap.release()
cv.destroyAllWindows()

