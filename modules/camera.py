import cv2
import numpy as np
import os
import subprocess

def take_photo():
  # 一時ファイルに画像を保存せずに取得するためのコマンド
  cmd = ['libcamera-still', '-n', '-o', '-', '--encoding', 'jpg']
  result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  
  # 画像をメモリ上に読み込む
  img_array = np.frombuffer(result.stdout, dtype=np.uint8)
  # OpenCVを使用して画像を読み込む
  img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

  cv2.imwrite("modules/photo.jpg", img)
 

