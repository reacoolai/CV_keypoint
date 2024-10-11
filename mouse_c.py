import cv2
import mediapipe as mp
import torch
import numpy as np
import asyncio
from depth_anything_v22.dpt import DepthAnythingV2
from mouse import MouseController, euclidean_distance

# 初始化 Mediapipe 和深度估计模型
mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
hands = mpHands.Hands()
controller = MouseController()

DEVICE = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'
model_configs = {
    'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
    'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
    'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
    'vitg': {'encoder': 'vitg', 'features': 384, 'out_channels': [1536, 1536, 1536, 1536]}
}

depth_model = DepthAnythingV2(**model_configs['vits'])
depth_model.load_state_dict(torch.load(f'checkpoints/depth_anything_v2_vits.pth', map_location='cpu'))
depth_model = depth_model.to(DEVICE).eval()


# 异步深度估计函数
async def estimate_depth(image):
    depth_map = depth_model.infer_image(image)
    depth_map = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    return depth_map


# 异步 Mediapipe 手势检测函数
async def detect_hand_landmarks(image):
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    return results


# 将 Mediapipe 关键点与深度图结合，生成3D关键点
def generate_3d_keypoints(hand_landmarks, depth_map, image_width, image_height):
    # 调整深度图大小，使其与输入图像大小一致
    depth_map_resized = cv2.resize(depth_map, (image_width, image_height))

    keypoints_3d = []
    for lm in hand_landmarks.landmark:
        # 将 Mediapipe 的 x, y 坐标转换为图像中的像素坐标
        x_pixel = int(lm.x * image_width)
        y_pixel = int(lm.y * image_height)

        # 从调整后的深度图中获取对应像素点的深度信息
        try:
            z_depth = depth_map_resized[y_pixel, x_pixel] / 255.0  # 归一化深度值
        except IndexError:
            continue
        # 生成 (x, y, z) 3D 坐标
        keypoints_3d.append((lm.x, lm.y, z_depth))
    return keypoints_3d


# 更新鼠标位置和点击功能
def update_mouse_control(hand_landmarks, image_width, image_height):
    finger_tip = hand_landmarks.landmark[8]  # 食指指尖
    thumb_tip = hand_landmarks.landmark[4]  # 拇指指尖

    # 将 Mediapipe 2D坐标转为像素坐标
    finger_x, finger_y = int(finger_tip.x * image_width), int(finger_tip.y * image_height)
    thumb_x, thumb_y = int(thumb_tip.x * image_width), int(thumb_tip.y * image_height)

    # 获取当前鼠标位置
    mouse_x, mouse_y = controller.get_mouse_position()

    # 移动鼠标
    controller.move(mouse_x + (finger_x - mouse_x), mouse_y + (finger_y - mouse_y))

    # 如果食指与拇指的距离很近，则模拟点击
    if euclidean_distance(finger_tip, thumb_tip) < 0.05:
        controller.click()


# 处理每一帧图像，结合深度信息和 Mediapipe 手势检测
async def process_frame(image):
    depth_task = asyncio.create_task(estimate_depth(image))  # 异步深度图任务
    mediapipe_task = asyncio.create_task(detect_hand_landmarks(image))  # 异步Mediapipe手势检测任务

    depth_map = await depth_task  # 等待深度图结果
    hand_results = await mediapipe_task  # 等待手势检测结果

    return depth_map, hand_results


async def main():
    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        image_height, image_width, _ = frame.shape
        depth_map, hand_results = await process_frame(frame)

        # 如果检测到了手势关键点
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                # 生成3D关键点
                keypoints_3d = generate_3d_keypoints(hand_landmarks, depth_map, image_width, image_height)

                # 绘制2D关键点和连接线
                mpDraw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)

                # 更新鼠标控制
                update_mouse_control(hand_landmarks, image_width, image_height)

        # 将RGB图像与深度图并排显示
        combined_result = np.hstack((frame, cv2.cvtColor(depth_map, cv2.COLOR_GRAY2BGR)))
        cv2.imshow("RGB + Depth + Mouse Control", combined_result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# 启动异步主函数
if __name__ == "__main__":
    asyncio.run(main())
