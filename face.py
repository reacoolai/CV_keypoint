import cv2
import mediapipe as mp
from playsound import playsound

face_mesh = mp.solutions.face_mesh.FaceMesh()
# hand_mesh = mp.solutions.hands.HandLandmark()
cap = cv2.VideoCapture(0)
# while cap.isOpened():
#     ret,frame = cap.read()
#     if ret == False:
#         break
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     result = face_mesh.process(rgb_frame)
#     if result.multi_face_landmarks:
#         for face in result.multi_face_landmarks:
#             for landmark in face.landmark:
#                 x = int(landmark.x*frame.shape[1])
#                 y = int(landmark.y*frame.shape[0])
#                 cv2.circle(frame,(x,y),1,(128,0,256))
#     # face_mesh.process(frame)
#     cv2.imshow('frame',frame)
#     cv2.waitKey(3)
while cap.isOpened():
    ret,frame = cap.read()
    if ret == False:
        break
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb_frame)
    if result.multi_face_landmarks:
        for face in result.multi_face_landmarks:
            for landmark in face.landmark:
                x = int(landmark.x*frame.shape[1])
                y = int(landmark.y*frame.shape[0])
                cv2.circle(frame,(x,y),3,(128,0,256))
    # face_mesh.process(frame)
    cv2.imshow('frame',frame)
    cv2.waitKey(3)