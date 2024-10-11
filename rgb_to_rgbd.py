import cv2
import torch
import numpy as np
from depth_anything_v22.dpt import DepthAnythingV2

# Set the device based on availability
DEVICE = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'

# Model configurations
model_configs = {
    'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
    'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
    'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
    'vitg': {'encoder': 'vitg', 'features': 384, 'out_channels': [1536, 1536, 1536, 1536]}
}

# Choose the encoder
encoder = 'vits'  # or 'vits', 'vitb', 'vitg'

# Load the model
model = DepthAnythingV2(**model_configs[encoder])
model.load_state_dict(torch.load(f'checkpoints/depth_anything_v2_{encoder}.pth', map_location='cpu'))
model = model.to(DEVICE).eval()

# Read the RGB image
raw_img = cv2.imread('your_img_path')

# Infer depth map from the image using the model
depth_map = model.infer_image(raw_img)  # HxW raw depth map in numpy

# Normalize depth map to range [0, 255] for visualization and combining with RGB
depth_map_normalized = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX)

# Convert depth map to a single channel 8-bit image
depth_map_normalized = depth_map_normalized.astype(np.uint8)

# Resize depth map to match RGB image dimensions (if needed)
depth_map_resized = cv2.resize(depth_map_normalized, (raw_img.shape[1], raw_img.shape[0]))

# Stack the RGB image (HxWx3) and the depth map (HxW) to create a 4-channel RGB-D image
rgb_d_image = np.dstack((raw_img, depth_map_resized))  # HxWx4

# Define a function to return the RGB-D image
def convert_to_rgbd_image(image_path, model):
    raw_img = cv2.imread(image_path)
    depth_map = model.infer_image(raw_img)  # Infer depth
    depth_map_normalized = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    depth_map_resized = cv2.resize(depth_map_normalized, (raw_img.shape[1], raw_img.shape[0]))
    rgb_d_image = np.dstack((raw_img, depth_map_resized))  # Combine RGB and depth into 4 channels
    return rgb_d_image

# Call the function and save the output as an RGB-D image
#输入需要转换的图片路径
rgb_d_image = convert_to_rgbd_image('your_img_path', model)

# Save the RGB-D image (optional)
output_path = 'your_out_img_path'
cv2.imwrite(output_path, rgb_d_image)

