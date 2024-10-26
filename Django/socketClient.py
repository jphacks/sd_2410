import socket
import requests
from django.http import JsonResponse
from django.conf import settings
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# URLとファイルパスの設定
url = "http://127.0.0.1:8000/api/mp3_openai/"
file_path = os.path.join(os.path.dirname(settings.BASE_DIR), "audio", "voice.wav")

# リクエストのデータとファイルを設定
files = {'filepath': open(file_path, 'rb')}

# POSTリクエストの送信
response = requests.post(url, files=files)

# レスポンス内容の出力
print(response.json()) 

# ソケットを作成
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# サーバーに接続
host = "10.0.0.195"  # サーバーのIPアドレス
port = 65432
client_socket.connect((host, port))
# 送信する文字列
message = response.json()['response']
client_socket.sendall(message.encode('utf-8'))
# ソケットを閉じる
client_socket.close()