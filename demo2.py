import cv2
import mediapipe as mp
from gf.down import img
from matplotlib import pyplot as plt
# 初始化 MediaPipe Pose 模型
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# 初始化 MediaPipe 绘制工具
mp_drawing = mp.solutions.drawing_utils

# 打开摄像头
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    # plt.imshow(frame)
    # 将图像转换为 RGB
    frame = cv2.flip(frame,1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 进行姿势检测
    results = pose.process(frame)

    # 绘制姿势关键点
    if results.pose_landmarks:
        for point in results.pose_landmarks.landmark:
            x, y = int(point.x * frame.shape[1]), int(point.y * frame.shape[0])
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

        # 绘制连接线
        for connection in mp_pose.POSE_CONNECTIONS:
            start_idx, end_idx = connection
            start_point = results.pose_landmarks.landmark[start_idx]
            end_point = results.pose_landmarks.landmark[end_idx]
            start_x, start_y = int(start_point.x * frame.shape[1]), int(start_point.y * frame.shape[0])
            end_x, end_y = int(end_point.x * frame.shape[1]), int(end_point.y * frame.shape[0])
            cv2.line(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

    # 将图像转换回 BGR
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    # aa = img(frame)
    # print(aa)

    # 显示图像
    cv2.imshow('Stick Figure', frame)

    # 按 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()