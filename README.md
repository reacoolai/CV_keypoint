## 🤗各类基于opencv和mediapipe的一些Demo。



![粘贴的图像 (3)](/home/reacool/文档/mydata/img/粘贴的图像 (3).png)

<video src="https://github.com/reacoolai/CV_keypoint/blob/main/img/9169b1b2a975806b611d1ba2104b6abd_raw.mp4"></video>

## Usage 

### Prepraration 

```pypthon
git clone https://github.com/reacoolai/CV_keypoint
pip install -r requirements.txt
```

### Running 

```python
python gui.py
```



基于深度预估模型depth-anything-v2和meidapipe结合的检测点增强。



![粘贴的图像 (2)](/home/reacool/文档/mydata/img/粘贴的图像 (2).png)

Depth-Anything-V2官方提供了4种模型，其中只有small模型的速度支持实时视频的检测。这里选择下载small模型。在 Depth-Anything-V2目录下创建一个checkpoints存放模型。

| Model                   | Params | Checkpoint                                                   |
| ----------------------- | ------ | ------------------------------------------------------------ |
| Depth-Anything-V2-Small | 24.8M  | [Download](https://huggingface.co/depth-anything/Depth-Anything-V2-Small/resolve/main/depth_anything_v2_vits.pth?download=true) |
| Depth-Anything-V2-Base  | 97.5M  | [Download](https://huggingface.co/depth-anything/Depth-Anything-V2-Base/resolve/main/depth_anything_v2_vitb.pth?download=true) |
| Depth-Anything-V2-Large | 335.3M | [Download](https://huggingface.co/depth-anything/Depth-Anything-V2-Large/resolve/main/depth_anything_v2_vitl.pth?download=true) |
| Depth-Anything-V2-Giant | 1.3B   | Coming soon                                                  |

### Running

```python
cd Depth-Anything-V2
python mouse_c.py		
```



这是一个尝试，如果有用到的地方还有很大的优化空间，这里只是实现这些想法🤗

参考项目

| 项目              | github                                             | 官网                                    |
| ----------------- | -------------------------------------------------- | --------------------------------------- |
| mediapipe         | https://github.com/google-ai-edge/mediapipe        | https://developers.google.com/mediapipe |
| Depth Anything V2 | https://github.com/DepthAnything/Depth-Anything-V2 |                                         |
