import socket
from .myapp.views.mp3 import mp3_view
# ソケットを作成
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# サーバーに接続
host = '127.0.0.1'  # サーバーのIPアドレス
port = 65432
client_socket.connect((host, port))
# 送信する文字列
message = mp3_view
client_socket.sendall(message.encode('utf-8'))
# ソケットを閉じる
client_socket.close()