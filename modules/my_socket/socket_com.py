import socket
import time
from modules.my_socket import my_config

# サーバーを立てて、テキスト取得したらサーバー閉じる
def start_server_getString(port=my_config.RASPBERRYPI_PORT):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # ポートの再利用オプションを設定
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(("0.0.0.0", port))
    server_socket.listen()
    print("Server started, waiting for connections...")

    # クライアントからの接続を待機
    server_socket.listen(1)
    print("クライアントからの接続を待っています...")

    # 接続を受け入れる
    client_socket, addr = server_socket.accept()
    print(f"接続を受け入れました: {addr}")

    # データを受信
    data = client_socket.recv(1024)
    print(f"受信したデータ: {data.decode('utf-8')}")

    # ソケットを閉じる
    time.sleep(0.5)
    server_socket.close()

    return data.decode('utf-8')

# クライアント接続して、文字を送って接続解除
def start_client_sendString(message, host=my_config.UNITY_ADDR, port=my_config.UNITY_PORT):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.sendall(message.encode('utf-8'))
    client_socket.close()