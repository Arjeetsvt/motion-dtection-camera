import threading
import winsound

import cv2
import imutils

backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_VFW, cv2.CAP_V4L2]

cap = None
for backend in backends:
    cap = cv2.VideoCapture(0, backend)
    if cap.isOpened():
        break

if not cap.isOpened():
    print("Error: Could not access the webcam with any backend.")
    exit()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

ret, start_frame = cap.read()
if not ret:
    print("Error: Could not read frame from webcam.")
    cap.release()
    cv2.destroyAllWindows()
    exit()

_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21,21), 0)

alram = False
alarm_mods = False
alarm_counter = 0

def alarm_sound():
    global alarm
    for _ in range(5):
        if not alarm_mods:
            break
        print("alarm")
        winsound.Beep(2500, 1000)
    alarm = False

while True:
     ret, frame = cap.read()
     if not ret:
          print("Error: Could not read frame from webcam.")
          break
     frame = imutils.resize(frame, width=500)

     if alarm_mods:
        frame_bw =cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw =cv2.GaussianBlur(frame_bw, (5, 5), 0)

        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw

        if threshold.sum() > 500:
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1
        
        cv2.imshow("Cam", threshold)
     else:
        cv2.imshow("Cam", frame)

     if alarm_counter > 20:
        if not alarm:
            alarm = True
            threading.Thread(target=alarm_sound).start()

        key_press = cv2.waitkey(30)
        if key_press == ord("t"):
            alarm_mods = not alarm_mods
            alarm_counter = 0
        if key_press == ord("q"):
            alarm_mods = False
            break

cap.release()
cv2.destroyAllWindows()










