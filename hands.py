# 导入所需要的库
import cv2
import mediapipe as mp
import numpy as np
import time
import Xlib.display
import Xlib.X
import Xlib.XK
import ctypes
import math
from mouse import MouseController
display = Xlib.display.Display()
root = display.screen().root
# 打开摄像头
cap = cv2.VideoCapture(0)
# 定义手部检测对象
mpHands = mp.solutions.hands
hands = mpHands.Hands()
first = True
mpDraw = mp.solutions.drawing_utils
click1 = 0
import time
def min_triangle_area(X, Y, Z):
    """
    计算由三个三维点X、Y、Z形成的三角形的面积

    参数:
    X, Y, Z: 包含x、y、z属性的点对象

    返回:
    三角形的面积
    """
    try:
        # 计算三边长度
        a = euclidean_distance(Y, Z)
        b = euclidean_distance(X, Z)
        c = euclidean_distance(X, Y)

        # 使用海伦公式计算面积
        s = (a + b + c) / 2  # 半周长
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))

        return area
    except AttributeError:
        raise AttributeError("X、Y和Z必须都包含x、y、z属性")
def euclidean_distance(X, Y):
    """
    计算两个三维点X和Y之间的欧式距离

    参数:
    X: 包含x、y、z属性的第一个点对象
    Y: 包含x、y、z属性的第二个点对象

    返回:
    两点之间的欧式距离
    """
    try:
        dx = X.x - Y.x
        dy = X.y - Y.y
        dz = X.z - Y.z

        distance = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
        return distance
    except AttributeError:
        raise AttributeError("X和Y必须都包含x、y、z属性")
str_time = time.time()
a = 0
while True:
    a = a+1
    if time.time() - str_time>=1:
        print(a)
        a = 0
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
            mouse_x, mouse_y = root.query_pointer()._data["root_x"], root.query_pointer()._data["root_y"]
            offset_x = -(last_X-hand.landmark[4].x)*distance_mouse

            offset_y = -(last_Y-hand.landmark[4].y)*distance_mouse
            # print(offset_x)
            # print(euclidean_distance(hand.landmark[4], hand.landmark[8]))
            if euclidean_distance(hand.landmark[4], hand.landmark[8]) < 0.04:
                root.warp_pointer(int(mouse_x + offset_x), int(mouse_y + offset_y))
            # print(min_triangle_area(hand.landmark[4], hand.landmark[8],hand.landmark[12]))

            display.sync()
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