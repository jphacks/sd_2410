import socket
import threading

# クライアント接続して、文字を送って接続解除
def start_client_sendString(message, host="10.0.0.192", port=65432):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.sendall(message.encode('utf-8'))