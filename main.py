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


# /home/izumi/Desktop/git/sd_2410/my_socket/my_config.py
# ソケット通信のIPアドレス設定忘れずに

# VPNのIPアドレス設定(ToDo)
# /home/izumi/Desktop/git/sd_2410/Unity/socket_send_msg.py
# /home/izumi/Desktop/git/sd_2410/my_socket/my_config.py

# デモ用 テレビ付けるのに7sかかるため、最初に起動
# subprocess.run("echo 'on 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
# print("TV on")

# 作成したモジュール(Todo モジュールファイルへの移動)
import camera            # 写真を撮って保存
import BrightnessChecker # 部屋の明るさチェック
import rec               # レコード開始
from my_socket import socket_com # ソケット通信
from bedtime_reminder import is_remind_time

start = time.time()
now = datetime.datetime.now() 
current_time = int(now.strftime("%H%M"))  # 現在時間取得 1713

sleep_duration = 7  # 何時間寝たいか

def status_csv_write(status, times, alarm, filename='modules/status.csv'):
    # 先頭に追加する行をデータフレームで作成
    new_row = pd.DataFrame([[status, times, alarm]], columns=['status', 'times', 'alarm'])
    # 既存のCSVファイルを読み込み
    existing_data = pd.read_csv(filename)
    # 新しい行と既存のデータを結合
    updated_data = pd.concat([new_row, existing_data], ignore_index=True)
    # 上書き保存
    updated_data.to_csv(filename, index=False)


def status_csv_read(filename='modules/status.csv'):
    # CSVファイルの最初の1行だけを読み込む
    first_row = pd.read_csv(filename, nrows=1)
    
    # それぞれのカラムから値を取得
    current_status = first_row['status'].iloc[0]
    times = first_row['times'].iloc[0]
    current_alarm = first_row['alarm'].iloc[0]
    
    return current_status, times, current_alarm

# ステータス確認
current_status, times, current_alarm = status_csv_read()

# 状態 wakeup_standby,0,セットしたアラーム時間 就寝中||起床前
if current_status == 'wakeup_standby' and times == 0 and current_alarm > current_time:
    print("就寝中")

# 状態 wakeup_standby,0~n,次のアラーム時間 起床すべき時間
elif current_status == 'wakeup_standby' and times >= 0 and current_alarm <= current_time:
    okita = "0" # 初期化
    camera.take_photo() # take photo

    # 画像を読投げて起きてるか判断   
    url = "http://127.0.0.1:8000/api/image_openai/"
    response = requests.post(url)
    print("response", response.json()) # Debug
    try:
        okita = response.json().split(": ")[1].strip(" \n}")
    except:
        okita = response.json().split(":")[1].strip("}")
    print("\n起きた:1 寝てる:0 →", okita)  # 起きてた：1/寝てた：0
    okita = "0" # デモ用(無条件で寝てると判断)

    if(okita == "0"):
        print("まだ寝てると判断")
        subprocess.run("echo 'on 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
        print("TV on")
        time.sleep(5)

        #TKD-スヌーズ機能用-----------------------
        url = f"http://127.0.0.1:8000/api/wake_up/{times}/"
        response = requests.post(url)
        # print("response", response)
        wake_up_string = response.json().get('answer')
        # print("wake_up_string", wake_up_string)
        socket_com.start_client_sendString(wake_up_string) 
        ####################################################
        #####        起こすずんだもん起動         ######
        ####################################################
        socket_com.start_server_getString(65432) # サーバー立てて文字取得まで待機

        subprocess.run("echo 'standby 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
        print("TV off")

        # csv書き換え
        times += 1
        status_csv_write('wakeup_standby', times, current_time +5)

        #30分間起きなかったら、slackに寝てる写真が送られる。
        if times == 6:
            url = "http://127.0.0.1:8000/api/send_image/"
            response = requests.get(url)

    elif(okita == "1"):
        print("起きたと判断")
        subprocess.run("echo 'on 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
        print("TV on")

        status_csv_write('wokeup', 1, 9999) # 起きたのでcsv書き換え

        url = "http://127.0.0.1:8000/api/search_today/"
        response = requests.get(url)
        print("response", response.json())
        socket_com.start_client_sendString(response) # Todo 今日の予定も？
        ####################################################
        ##### 　　　Unityからうんちくずんだもん起動      ######
        ####################################################
        socket_com.start_server_getString(65432) # サーバー立てて文字取得まで待機

        subprocess.run("echo 'standby 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
        print("TV off")

        status_csv_write('wokeup', 2, 9999) # 起きたのでcsv書き換えて終了


# 状態 wokeup,2,9999 外出中
elif current_status == 'wokeup' and times == 2 and current_alarm == 9999:

    camera.take_photo() # take photo
    # check goout/inhome
    if BrightnessChecker.homeChecker(): # true -> in home
    # if True: # デモ用(無条件で帰宅状態に)
        subprocess.run("echo 'on 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
        print("TV on")
        time.sleep(0.5) # テレビつくのを待つ(デモ用に短く設定)

        socket_com.start_client_sendString("おかえり、明日は何時に起こせばいいのだ？") # サーバー接続して文字送信
        ####################################################
        #####         Unityから起床時間の質問        ######
        ####################################################
        socket_com.start_server_getString(65432) # サーバー立てて文字取得まで待機

        rec.recording()                     # recordingスタート
        url = "http://127.0.0.1:8000/api/mp3_openai/"
        response = requests.post(url)
        
        set_alarm = int(response.json()['time']) # 起床時間
        status_csv_write('wokeup', 3, set_alarm)
        response_line = response.json()['response'] # 喋るセリフ

        socket_com.start_client_sendString(response_line) # サーバー接続して文字送信
        ####################################################
        #####          Unityから起床時間の復唱       ######
        ####################################################
        socket_com.start_server_getString(65432) # サーバー立てて文字取得まで待機

        subprocess.run("echo 'standby 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
        print("TV standby")
    else:
        print("外出中")

# 状態睡眠催促すべき状態
elif current_status == 'wokeup' and times == 3:
    alarm_time_str = str(current_alarm).zfill(4) # 0でパディング，例：600を0600に
    if is_remind_time(alarm_time_str, sleep_duration, 5, "2300"):
        url = f"http://127.0.0.1:8000/api/sleep_remind/?alarm_time={alarm_time_str}&sleep_duration={sleep_duration}"
        response = requests.get(url)
        print(response.json()["answer"])

# 状態 wokeup,3,セットしたアラーム時間 日付またぎ(アラーム時間と現在時間を大小比較するため)
elif current_status == 'wokeup' and times == 3 and current_alarm == 9999:
    if "0000" <= current_time <= "0015": # 冗長
        status_csv_write('wakeup_standby', 0, current_alarm)
