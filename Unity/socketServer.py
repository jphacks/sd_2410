import socket

def getString_socket():
    # ソケットを作成
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # バインドするアドレスとポート
    host = socket.gethostbyname(socket.gethostname())  # localhost
    port = 65432
    server_socket.bind((host, port))

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
    client_socket.close()
    server_socket.close()
    
    return data.decode('utf-8')

getString_socket()
