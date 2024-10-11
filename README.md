<br>             
<br>
<div align="center">
<h1>🤗关于关键点检测的一些Demo</h1>
<br>
</div>
<br>
<br><br>

<img src='https://github.com/reacoolai/CV_keypoint/blob/main/img/3.png'>


<video src="https://github.com/reacoolai/CV_keypoint/blob/main/img/9169b1b2a975806b611d1ba2104b6abd_raw.mp4"></video>

## Usage 

### Prepraration 

```pypthon
git clone https://github.com/reacoolai/CV_keypoint
cd CV_keypoint
pip install -r requirements.txt
```

### Running 

```python
python gui.py
```



基于深度预估模型depth-anything-v2和meidapipe结合的检测点增强。


<img src='https://github.com/reacoolai/CV_keypoint/blob/main/img/2.png'>

Depth-Anything-V2官方提供了4种模型，其中只有small模型的速度支持实时视频的检测。这里选择下载small模型。在 Depth-Anything-V2目录下创建一个checkpoints存放模型。

| Model                   | Params | Checkpoint                                                   |
| ----------------------- | ------ | ------------------------------------------------------------ |
| Depth-Anything-V2-Small | 24.8M  | [Download](https://huggingface.co/depth-anything/Depth-Anything-V2-Small/resolve/main/depth_anything_v2_vits.pth?download=true) |
| Depth-Anything-V2-Base  | 97.5M  | [Download](https://huggingface.co/depth-anything/Depth-Anything-V2-Base/resolve/main/depth_anything_v2_vitb.pth?download=true) |
| Depth-Anything-V2-Large | 335.3M | [Download](https://huggingface.co/depth-anything/Depth-Anything-V2-Large/resolve/main/depth_anything_v2_vitl.pth?download=true) |
| Depth-Anything-V2-Giant | 1.3B   | Coming soon                                                  |

### Running

```python

python mouse_c.py		
```
RGB摄像头图像转换为深度摄像头的图像


```python

python rgb_to_rgbd.py
```
###  Running 
在图像上运行脚本
```python
python run.py \
  --encoder <vits | vitb | vitl | vitg> \
  --img-path <path> --outdir <outdir> \
  [--input-size <size>] [--pred-only] [--grayscale]
```
Options: 选项：

    --img-path: You can either 1) point it to an image directory storing all interested images, 2) point it to a single image, or 3) point it to a text file storing all image paths.
    --img-path ：您可以 1) 将其指向存储所有感兴趣图像的图像目录，2) 将其指向单个图像，或 3) 将其指向存储所有图像路径的文本文件。
    --input-size (optional): By default, we use input size 518 for model inference. You can increase the size for even more fine-grained results.
    --input-size （可选）：默认情况下，我们使用输入大小518进行模型推理。您可以增加大小以获得更细粒度的结果。
    --pred-only (optional): Only save the predicted depth map, without raw image.
    --pred-only (可选): 只保存预测的深度图，不保存原始图像。
    --grayscale (optional): Save the grayscale depth map, without applying color palette.
    --grayscale （可选）：保存灰度深度图，不应用调色板。
这是一个尝试，如果有用到的地方还有很大的优化空间，这里只是实现这些想法🤗

参考项目

| 项目              | github                                             | 官网                                    |
| ----------------- | -------------------------------------------------- | --------------------------------------- |
| mediapipe         | https://github.com/google-ai-edge/mediapipe        | https://developers.google.com/mediapipe |
| Depth Anything V2 | https://github.com/DepthAnything/Depth-Anything-V2 |                                         |



