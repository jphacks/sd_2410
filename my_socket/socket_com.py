import socket
import threading
# import my_config

# サーバーを立てて、テキスト取得したらサーバー閉じる
def start_server_getString():
# def start_server_getString(host=my_config.SERVER_PC_IP, port=my_config.PORT):
    server_socket = socket.socket(socket.AF_INET, socket.SO_VM_SOCKETS_BUFFER_MIN_SIZE)
    server_socket.bind(("0.0.0.0", 65432))
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
    server_socket.close()

    return data.decode('utf-8')

# クライアント接続して、文字を送って接続解除
def start_client_sendString(message, host="10.0.0.196", port=65432):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.sendall(message.encode('utf-8'))
    client_socket.close()