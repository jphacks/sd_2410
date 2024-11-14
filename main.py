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

# デモ用 テレビ付けるのに7sかかるため、最初に起動
# subprocess.run("echo 'on 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
# print("TV on")

# 作成したモジュール(Todo モジュールファイルへの移動)
from modules import camera            # 写真を撮って保存
from modules import BrightnessChecker # 部屋の明るさチェック
from modules import rec               # レコード開始
from modules.my_socket import socket_com # ソケット通信
from modules.my_socket import my_config
from modules.bedtime_reminder import is_remind_time
from modules.google_calender_api import get_events_today

start = time.time()
now = datetime.datetime.now() 
current_time = int(now.strftime("%H%M"))  # 現在時間取得 1713
is_runging_on_rasp = False # ラズパイで動かす時はTrue，ローカルでテストするときはFalse


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

def send_to_unity_and_wait(message):
        socket_com.start_client_sendString(message, port=my_config.UNITY_PORT) 
        return socket_com.start_server_getString(port=my_config.RASPBERRYPI_PORT) # サーバー立てて文字取得まで待機


# ステータス確認
current_status, times, current_alarm = status_csv_read()

# 状態 wakeup_standby,0,セットしたアラーム時間 就寝中||起床前
if current_status == 'wakeup_standby' and times == 0 and current_alarm > current_time:
    print("就寝中")

# 状態 wakeup_standby,0~n,次のアラーム時間 起床すべき時間
elif current_status == 'wakeup_standby' and times >= 0 and current_alarm <= current_time:
    okita = "0" # 初期化
    if is_runging_on_rasp: 
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
    okita = "1" # デモ用(無条件で寝てると判断)

    if(okita == "0"):
        print("まだ寝てると判断")
        if is_runging_on_rasp:
            subprocess.run("echo 'on 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
            time.sleep(5)
        print("TV on")

        times += 1

        # -スヌーズ機能用-----------------------
        url = f"http://127.0.0.1:8000/api/wake_up/{times}/"
        response = requests.post(url)
        wake_up_string = response.json().get('answer')
        sent_to_unity_message = f"{times}:{wake_up_string}"
        print("wake_up_string", wake_up_string)
        send_to_unity_and_wait(sent_to_unity_message)
        ####################################################
        #####        Unity起こすずんだもん起動         ######
        ####################################################

        if is_runging_on_rasp:
            subprocess.run("echo 'standby 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
        print("TV off")

        # csv書き換え
        status_csv_write('wakeup_standby', times, current_time +5)

        #30分間起きなかったら、slackに寝てる写真が送られる。
        if times == 6:
            url = "http://127.0.0.1:8000/api/send_image/"
            response = requests.get(url)

    elif(okita == "1"):
        print("起きたと判断")
        if is_runging_on_rasp:
            subprocess.run("echo 'on 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
        print("TV on")

        url = "http://127.0.0.1:8000/api/search/"
        data = get_events_today() # api側はこのdataを使っていない．指定する必要は？
        response = requests.post(url, json=data)
        print("response", response.json()['answer']) 
        send_to_unity_and_wait(response.json()['answer']) # Todo 今日の予定も？
        ####################################################
        ##### 　　　Unityから蘊蓄/予定ずんだもん起動      ######
        ####################################################

        if is_runging_on_rasp:
            subprocess.run("echo 'standby 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
        print("TV off")

        status_csv_write('wokeup', 1, 9999) # 起きたのでcsv書き換えて終了


# 状態 wokeup,1,9999 外出中
elif current_status == 'wokeup' and times == 1 and current_alarm == 9999 and current_time > 1300: # 13時以降帰宅想定

    if is_runging_on_rasp:
        camera.take_photo() # take photo
    # check goout/inhome
    if BrightnessChecker.homeChecker(): # true -> in home
    # if True: # デモ用(無条件で帰宅状態に)
        if is_runging_on_rasp:
            subprocess.run("echo 'on 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
            time.sleep(0.5) # テレビつくのを待つ(デモ用に短く設定)
        print("TV on")

        # message = "おかえり、明日は何時に起こせばいいのだ？"
        url = "http://127.0.0.1:8000/api/welcome_back/"
        message = requests.get(url).json()['answer']


        send_to_unity_and_wait(message)

        ####################################################
        #####         Unityから起床時間の質問        ######
        ####################################################

        rec.recording()                     # recordingスタート
        url = "http://127.0.0.1:8000/api/mp3_openai/"
        response = requests.post(url)
        
        set_alarm = int(response.json()['time']) # 起床時間
        status_csv_write('wokeup', 2, set_alarm)
        response_line = response.json()['response'] # 喋るセリフ

        send_to_unity_and_wait(response_line)
        ####################################################
        #####          Unityから起床時間の復唱       ######
        ####################################################

        if is_runging_on_rasp:
            subprocess.run("echo 'standby 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
        print("TV standby")
    else:
        print("外出中")

# 状態睡眠催促すべき状態
elif current_status == 'wokeup' and times == 2:
    alarm_time_str = str(current_alarm).zfill(4) # 0でパディング，例：600を0600に
    remind_list = [9, 8, 7, 6] # 何時間前にリマインドするかのリスト

    for sleep_duration in remind_list:
        if is_remind_time(alarm_time_str, sleep_duration, 5, "2300"): # 実際に使うときは2300を消す
            if is_runging_on_rasp:
                subprocess.run("echo 'on 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
            print("TV on")

            url = f"http://127.0.0.1:8000/api/sleep_remind/?alarm_time={alarm_time_str}&sleep_duration={sleep_duration}"
            response = requests.get(url)
            message = response.json()['answer']
            print(message)

            send_to_unity_and_wait(message)
            ####################################################
            #####          アバターが睡眠催促       ######
            ####################################################

            if is_runging_on_rasp:
                subprocess.run("echo 'standby 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
            print("TV standby")

# 状態 wokeup,3,セットしたアラーム時間 日付またぎ(アラーム時間と現在時間を大小比較するため)
elif current_status == 'wokeup' and times == 3 and current_alarm == 9999:
    if "0000" <= current_time <= "0010": # 冗長
        status_csv_write('wakeup_standby', 0, current_alarm)
