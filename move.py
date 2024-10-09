# 导入所需要的库
import cv2
import mediapipe as mp
import numpy as np
import time


from mouse import MouseController,min_triangle_area,euclidean_distance
# 打开摄像头
cap = cv2.VideoCapture(0)
# 定义手部检测对象
mpHands = mp.solutions.hands
hands = mpHands.Hands()
first = True
mpDraw = mp.solutions.drawing_utils
click1 = 0


str_time = time.time()
pin_S = 0
l2_min = 0
last_l2 = True
l3_min = 0
last_l3 = True
controller = MouseController()
while True:
    pin_S = pin_S+1
    if time.time() - str_time>=1:
        print(pin_S)
        pin_S = 0
        str_time = time.time()
    # 读取一帧图像
    success, img = cap.read()
    if not success:
        continue
    img = cv2.flip(img,1)
    image_height, image_width, _ = np.shape(img)
    # 转为rgb
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 得到检测结果
    results = hands.process(imgRGB)
    distance_mouse = 1000
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            # 打印手指坐标
            if first:
                first = False
                last_X = hand.landmark[4].x
                last_Y = hand.landmark[4].y
                # print(1)
            mouse_x, mouse_y = controller.get_mouse_position()
            offset_x = -(last_X-hand.landmark[4].x)*distance_mouse

            offset_y = -(last_Y-hand.landmark[4].y)*distance_mouse
            # print(offset_x)
            # print(euclidean_distance(hand.landmark[4], hand.landmark[8]))
            l2 = euclidean_distance(hand.landmark[4], hand.landmark[8])
            if l2 < 0.04:
                if last_l2 and l2_min > 0:
                    l2_min = 0
                    print('click')
                    controller.click()
                if last_l2 ==True:
                    l2_min = 10
                    last_l2 = False
                if l2_min>0:
                    l2_min = l2_min-1

                controller.move(int(mouse_x + offset_x), int(mouse_y + offset_y))
            else:
                last_l2 = True
            # print(min_triangle_area(hand.landmark[4], hand.landmark[8],hand.landmark[12]))
            l3 = euclidean_distance(hand.landmark[4],  hand.landmark[12])
            if l3 < 0.04:
                l3_min = l3_min+1
                if l2_min >10:
                    controller.start_press()
                if last_l3 ==True:
                    # controller.start_press()
                    last_l3 = False

                controller.move(int(mouse_x + offset_x), int(mouse_y + offset_y))
            else:
                l3_min = 0
                last_l3 = True

                controller.stop_press()
            last_X = hand.landmark[4].x
            last_Y = hand.landmark[4].y
            # print("\r%.2f %.2f " % (
            # # hand.landmark[0].z, hand.landmark[4].z, hand.landmark[8].z, hand.landmark[12].z, hand.landmark[16].z,
            # hand.landmark[4].x,hand.landmark[8].x))
            mpDraw.draw_landmarks(img, hand, mpHands.HAND_CONNECTIONS)
    cv2.imshow("hands", img)
    key = cv2.waitKey(1) & 0xFF
    # 按q推出
    if key == ord('q'):
        break
cap.release()
