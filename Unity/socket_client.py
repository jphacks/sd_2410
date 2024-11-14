import socket
import threading
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from sd_2410.modules.my_socket import my_config

# クライアント接続して、文字を送って接続解除
def start_client_sendString(message, host=my_config.RASPBERRYPI_ADDR, port=my_config.RASPBERRYPI_PORT):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.sendall(message.encode('utf-8'))