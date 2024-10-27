import cv2
import datetime
import time
import tempfile
import numpy as np
import os
import subprocess
import pandas as pd
import requests

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 作成したもの
import camera            # take photo
import BrightnessChecker # check goout/inhome
import rec              # record get up time
from my_socket import socket_com # ソケット通信

start = time.time()
now = datetime.datetime.now() 
current_time = int(now.strftime("%H%M"))  # 現在時間取得 1713


subprocess.run("echo 'on 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
print("TV on")


def status_csv_write(status, times, alarm, filename='status.csv'):
    # 先頭に追加する行をデータフレームで作成
    new_row = pd.DataFrame([[status, times, alarm]], columns=['status', 'times', 'alarm'])
    # 既存のCSVファイルを読み込み
    existing_data = pd.read_csv(filename)
    # 新しい行と既存のデータを結合
    updated_data = pd.concat([new_row, existing_data], ignore_index=True)
    # 上書き保存
    updated_data.to_csv(filename, index=False)


def status_csv_read(filename='status.csv'):
    # CSVファイルの最初の1行だけを読み込む
    first_row = pd.read_csv(filename, nrows=1)
    
    # それぞれのカラムから値を取得
    current_status = first_row['status'].iloc[0]
    times = first_row['times'].iloc[0]
    current_alarm = first_row['alarm'].iloc[0]
    
    return current_status, times, current_alarm

# ステータス確認
current_status, times, current_alarm = status_csv_read()

# 起床前
if current_status == 'A' and times == 0 and current_alarm > current_time:
    print("就寝中")

# 起床すべき時間
elif current_status == 'A' and times >= 0 and current_alarm <= current_time:
    okita = "0" # 初期化
    camera.take_photo() # take photo

    ###########################################
    #####   画像を読み込んで起きてるか判断   ######
    ##########################################
    url = "http://127.0.0.1:8000/api/image_openai/"
    response = requests.post(url)
    # print("response", response.json()) # Debug
    okita = response.json().split(": ")[1].strip(" \n}")
    print("\n起きた:1 寝てる:0 →", okita)  # 起きてた：1/寝てた：0

    if(okita == "0"):
        print("まだ寝てると判断")
        subprocess.run("echo 'on 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
        print("TV on")
        time.sleep(5)

        socket_com.start_client_sendString("起きる時間なのだ。早くベッドから出るのだ。早くずんだ餅食べたいのだ。") # サーバー接続して文字送信
        ####################################################
        ##### 起こすずんだもん起動   ######
        ####################################################
        socket_com.start_server_getString(65432) # サーバー立てて文字取得まで待機

        subprocess.run("echo 'standby 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
        print("TV off")

        # csv書き換え
        times += 1
        status_csv_write("A", times, current_time +5)

    elif(okita == "1"):
        print("起きたと判断")
        subprocess.run("echo 'on 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
        print("TV on")

        status_csv_write("B", 1, 9999) # 起きたのでcsv書き換え

        socket_com.start_client_sendString("今日8月20日はずんだ餅の日なのだ") # サーバー接続して文字送信
        ####################################################
        ##### I/O なし/実行終了合図      ######
        ##### うんちくずんだもん起動      ######
        ####################################################
        socket_com.start_server_getString(65432) # サーバー立てて文字取得まで待機

        subprocess.run("echo 'standby 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
        print("TV off")

        status_csv_write("B", 2, 9999) # 起きたのでcsv書き換えて終了


# 外出中
elif current_status == 'B' and times == 2 and current_alarm == 9999:

    # camera.take_photo() # take photo
    # check goout/inhome
    # if BrightnessChecker.homeChecker():
    if True:
        # true -> in home
        # subprocess.run("echo 'on 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
        # print("TV on")
        time.sleep(1) # テレビつくのを待つ

        socket_com.start_client_sendString("おかえりなのだ。明日何時起きるのか教えるのだ。") # サーバー接続して文字送信
        ####################################################
        ##### 起床時間質問Unity  ######
        ####################################################
        socket_com.start_server_getString(65432) # サーバー立てて文字取得まで待機

        rec.recording()                     # recordingスタート
        url = "http://127.0.0.1:8000/api/mp3_openai/"
        response = requests.post(url)
        
        set_alarm = int(response.json()['time']) # 起床時間
        status_csv_write("B", 3, set_alarm)
        response_line = response.json()['response'] # 喋るセリフ

        socket_com.start_client_sendString(response_line) # サーバー接続して文字送信
        ####################################################
        ##### 起床時間確認Unity  ######
        ####################################################
        socket_com.start_server_getString(65432) # サーバー立てて文字取得まで待機

        subprocess.run("echo 'standby 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
        print("TV standby")
    else:
        print("外出中")

# 日付またぎ(アラーム時間と現在時間を大小比較するため)
elif current_status == 'B' and times == 3 and current_alarm == 9999:
    if "0000" <= current_time <= "0030": # 冗長
        status_csv_write("A", 0, current_alarm)
