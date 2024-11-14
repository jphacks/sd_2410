import pandas as pd
import socket
import time
from modules.my_socket import my_config

def speaker_change(changed_speaker):
  df = pd.read_csv('modules/speaker.csv')
  changed_row = df['speaker_name'] == changed_speaker

  if changed_row.any():
    # その行を先頭に移動させる
    df = pd.concat([df[changed_row], df.drop(df[changed_row].index)])
    df.to_csv('modules/speaker.csv', index=False)
    print(f'スピーカーを{changed_speaker}に変更しました')


# サーバーを立てて、テキスト取得
def start_server_getString(port=my_config.RASPBERRYPI_PORT):
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # ポートの再利用オプションを設定
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  server_socket.bind(("0.0.0.0", port))
  server_socket.listen()
  print("Server started, waiting for connections...")

  while True:
    print("クライアントからの接続を待っています...")

    # クライアントからの接続を受け入れる
    client_socket, addr = server_socket.accept()
    print(f"接続を受け入れました: {addr}")

    # データを受信
    data = client_socket.recv(1024)
    data_decoded = data.decode('utf-8')
    # print(f"受信したデータ: {data_decoded}")

    # クライアント接続のみを閉じる
    client_socket.close()
    print("クライアント接続が終了しました。再度待機します。")

    # 受信データを使用して何か処理したい場合はここで行う
    speaker_change(data_decoded)

  # このコードではserver_socket.close()を呼ばないため、
  # サーバーは無限ループで開きっぱなしになります。

start_server_getString()
  