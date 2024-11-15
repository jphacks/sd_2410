import datetime
import time
import os
import subprocess
import pandas as pd
import requests
import cv2
import json
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))

is_runging_on_rasp = True # ラズパイで動かす時はTrue，ローカルでテストするときはFalse
# デモ用 テレビ付けるのに7sかかるため、最初に起動
# subprocess.run("echo 'on 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
# print("TV on")

# 作成したモジュール
from modules import camera                # 写真を撮って保存
from modules import BrightnessChecker     # 部屋の明るさチェック
from modules import rec                   # レコード開始
from modules.my_socket import socket_com  # ソケット通信
from modules.bedtime_reminder import is_remind_time
from modules.google_calender_api import get_events_today

start = time.time()
now = datetime.datetime.now() 
current_time = int(now.strftime("%H%M"))  # 現在時間取得 例)1713

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

def speaker_csv_read(filename='modules/speaker.csv'):
    # CSVファイルの最初の1行だけを読み込む
    first_row = pd.read_csv(filename, nrows=1)
    
    # それぞれのカラムから値を取得
    speaker_id = first_row['speaker_id'].iloc[0]
    speaker_name = first_row['speaker_name'].iloc[0]
    speaker_mate = first_row['speaker_mate'].iloc[0]
    system_prompt = first_row['system_prompt'].iloc[0]
    return speaker_id, speaker_name, speaker_mate, system_prompt

def send_to_unity_and_wait(message, times=-1):
    message = f"{times}:{speaker_id}:{message}"
    socket_com.start_client_sendString(message) 
    return socket_com.start_server_getString() # サーバー立てて文字取得まで待機

# ステータス確認
current_status, times, current_alarm = status_csv_read()
speaker_id, speaker_name, speaker_mate, system_prompt = speaker_csv_read()
user_name = "ケニー"

speaker_data = {
    'system_prompt' : system_prompt,
    'mate' : speaker_mate,
    'user_name': user_name
}

######################################  DEBUG  ######################################
# 111行目 okita も調整
current_status, times, current_alarm, current_time= 'wakeup_standby', 0,  700, 701  # 起床フェーズ (何もしない)
current_status, times, current_alarm, current_time= 'wakeup_standby', 1,  705, 706  # まだ寝てる 　
# current_status, times, current_alarm, current_time= 'wakeup_standby', 5,  730, 731  # まだ寝てる slack投稿フェーズ
# current_status, times, current_alarm, current_time= 'wakeup_standby', 1, 1000, 1005 # 起床蘊蓄も終了(帰宅待機)
# current_status, times, current_alarm, current_time= 'wokeup'        , 1, 9999, 1700 # 帰宅判断1回目 (部屋明るく)
# current_status, times, current_alarm, current_time= 'wokeup'        , 2,  700, 1800 # アラームセット完了 (何もしない)
# current_status, times, current_alarm, current_time= 'wokeup'        , 2,  700, 2200 # 睡眠催促
# current_status, times, current_alarm, current_time= 'wakeup_standby', 2,  700, 5    # 日付跨ぎ 

# send_to_unity_and_wait("リーチ！一発！ツモ！")
# time.sleep(10)
######################################  DEBUG  ######################################

# 状態 wakeup_standby,0,セットしたアラーム時間 就寝中||起床前
if current_status == 'wakeup_standby' and times == 0 and current_alarm > current_time:
    print("就寝中")

# 状態 wakeup_standby,0~n,次のアラーム時間 起床すべき時間
elif current_status == 'wakeup_standby' and times >= 0 and current_alarm <= current_time:
    okita = "0" # 初期化
    if is_runging_on_rasp: 
        camera.take_photo() # take photo

    # 画像を投げて起きてるか判断   
    url = "http://127.0.0.1:8000/api/image_openai/"
    response = requests.post(url)
    print("response", response.json()) # Debug
    try:
        okita = response.json().split(": ")[1].strip(" \n}")
    except:
        okita = response.json().split(":")[1].strip("}")
    print("\n起きた:1 寝てる:0 →", okita)  # 起きてた：1/寝てた：0
    # okita = "1" # デモ用(無条件で寝てると判断)

    if(okita == "0"):
        print("まだ寝てると判断")
        if is_runging_on_rasp:
            subprocess.run("echo 'on 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
            time.sleep(5)
        print("TV on")

        times += 1

        # -スヌーズ機能用-----------------------
        url = f"http://127.0.0.1:8000/api/wake_up/{times}/"
        response = requests.post(url, json=speaker_data)

        wake_up_string = response.json().get('answer')
        print("wake_up_string", wake_up_string)
        send_to_unity_and_wait(wake_up_string, times=times)
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
            print("slackに画像を投稿しました\n")

    elif(okita == "1"):
        print("起きたと判断")
        if is_runging_on_rasp:
            subprocess.run("echo 'on 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
        print("TV on")

        url = "http://127.0.0.1:8000/api/search/"
        event_data = get_events_today() # api側はこのdataを使っていない．指定する必要は？
        speaker_event_data = speaker_data
        speaker_event_data['event'] = "、".join(event_data)

        response = requests.post(url, json=speaker_event_data)
        print("response", response.json()['answer']) 
        send_to_unity_and_wait(response.json()['answer']) 
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

        url = "http://127.0.0.1:8000/api/welcome_back/"
        message = requests.post(url, json=speaker_data).json()['answer']

        send_to_unity_and_wait(message)
        ####################################################
        #####         Unityから起床時間の質問        ######
        ####################################################

        rec.recording()                     # recordingスタート
        url = "http://127.0.0.1:8000/api/mp3_openai/"
        response = requests.post(url, json=speaker_data)
        
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
        if is_remind_time(alarm_time_str, sleep_duration, 5, str(current_time)):  

            camera.take_photo() # 寝てるかどうかの判断のための写真
            if BrightnessChecker.homeChecker(): # true -> in home
                if is_runging_on_rasp:
                    subprocess.run("echo 'on 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
                print("TV on")

            url = f"http://127.0.0.1:8000/api/sleep_remind/"
            speaker_sleep_remind_data = speaker_data
            speaker_sleep_remind_data['alarm_time'] = alarm_time_str
            speaker_sleep_remind_data['sleep_duration'] = sleep_duration
            response = requests.post(url, json=speaker_sleep_remind_data)
            message = response.json()['answer']
            print(message)
            send_to_unity_and_wait(message)
            ####################################################
            #####          アバターが睡眠催促       ######
            ####################################################

            if is_runging_on_rasp:
                subprocess.run("echo 'standby 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
            print("TV standby")

# 状態 wokeup,2,セットしたアラーム時間 日付またぎ(アラーム時間と現在時間を大小比較するため)
elif current_status == 'wokeup' and times == 2 and current_alarm == 9999:
    if "0000" <= current_time <= "0010": # 冗長
        status_csv_write('wakeup_standby', 0, current_alarm)
