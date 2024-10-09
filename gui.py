import tkinter as tk
import subprocess
import threading

def run_script(script_path):
    # 执行指定的Python脚本
    subprocess.run(["/root/anaconda3/envs/shibie/bin/python", script_path])

def run_script_thread(script_path):
    # 使用多线程运行脚本
    thread = threading.Thread(target=run_script, args=(script_path,))
    thread.start()


root = tk.Tk()
root.title('Ruiku-Motion recognition software based on computer vision')
root.geometry('800x400')

# 设置背景颜色
root.configure(bg='lightblue')

# 创建按钮
button_gesture = tk.Button(root, text='手势识别', command=lambda: run_script_thread("/home/reacool/桌面/Demo/CV/move.py"))
button_gesture.pack(pady=20)

button_pose = tk.Button(root, text='姿势识别', command=lambda: run_script_thread("/home/reacool/桌面/Demo/CV/demo2.py"))
button_pose.pack(pady=20)

button_face = tk.Button(root, text='面部识别', command=lambda: run_script_thread("/home/reacool/桌面/Demo/CV/face.py"))
button_face.pack(pady=20)

button_game = tk.Button(root, text='GAME', command=lambda: run_script_thread("/home/reacool/桌面/Demo/CV/plane.py"))
button_game.pack(pady=20)

button_game2 = tk.Button(root, text='GAME2', command=lambda: run_script_thread("/home/reacool/桌面/Demo/CV/qieshuiguo.py"))
button_game2.pack(pady=20)

# 美化按钮
button_gesture.configure(bg='blue', fg='white', font=('Arial', 12))
button_pose.configure(bg='blue', fg='white', font=('Arial', 12))
button_face.configure(bg='blue', fg='white', font=('Arial',12))
button_game.configure(bg='blue', fg='white', font=('Arial', 12))
button_game2.configure(bg='blue', fg='white', font=('Arial', 12))

root.mainloop()