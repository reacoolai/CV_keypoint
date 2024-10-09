from Xlib import X, display
from Xlib.ext import xtest
import time
import math
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
class MouseController:
    def __init__(self):
        self.display = display.Display()
        self.root = self.display.screen().root

    def move(self, x, y):
        """移动鼠标到指定坐标"""
        xtest.fake_input(self.display, X.MotionNotify, x=x, y=y)
        self.display.sync()

    def click(self, button=1):
        """单击鼠标"""
        xtest.fake_input(self.display, X.ButtonPress, button)
        self.display.sync()
        time.sleep(0.1)
        xtest.fake_input(self.display, X.ButtonRelease, button)
        self.display.sync()

    def double_click(self, button=1):
        """双击鼠标"""
        self.click(button)
        time.sleep(0.1)
        self.click(button)

    def start_press(self, button=1):
        """长按鼠标"""
        xtest.fake_input(self.display, X.ButtonPress, button)
        self.display.sync()

        xtest.fake_input(self.display, X.ButtonRelease, button)
        self.display.sync()
    def stop_press(self, button=1):
        xtest.fake_input(self.display, X.ButtonRelease, button)
        self.display.sync()
    def get_mouse_position(self):
        """获取当前鼠标位置"""
        data = self.root.query_pointer()._data
        return data["root_x"], data["root_y"]

# def main():
#     controller = MouseController()
#
#     # 获取当前鼠标位置
#     current_x, current_y = controller.get_mouse_position()
#     print(f"当前鼠标位置: ({current_x}, {current_y})")
#
#     # 移动鼠标
#     print("移动鼠标到 (100, 100)")
#     controller.move(100, 100)
#     time.sleep(1)
#
#     print("执行单击")
#     controller.click()
#     time.sleep(1)
#
#     print("执行双击")
#     controller.double_click()
#     time.sleep(1)
#
#     print("执行长按（2秒）")
#     controller.long_press(2)
#
#     # 移回原位置
#     print(f"移动鼠标回原位置 ({current_x}, {current_y})")
#     controller.move(current_x, current_y)

if __name__ == "__main__":
    # main()
    pass