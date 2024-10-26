import cv2
import datetime
import time
import tempfile
import numpy as np
import os
import subprocess
import pandas as pd
import requests

base_path = "/home/izumi/Desktop/git/sd_2410/"
os.chdir(base_path)

# 作成したもの
import camera            # take photo
import BrightnessChecker # check goout/inhome
# import openai            # 未設定
import rec


start = time.time()
now = datetime.datetime.now() 
current_time = now.strftime("%H%M")  # 現在時間取得 1713

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
elif current_status == 'A' and times > 0 and current_alarm <= current_time:
    # 起床時刻と判断

    camera.take_photo() # take photo
    ####################################################
    ##### I/O 画像/okita(true/false)               ######
    ##### 画像を読み込んで起きてるか判断するpython実行   ######
    ####################################################
    okita == true
    
    if(not okita):
        # 起きてなければ以下を実行
        subprocess.run("echo 'on 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
        print("TV on")

        ####################################################
        ##### 起こすずんだもん起動   ######
        ####################################################

        # csv書き換え
        times += 1
        status_csv_write("A", times, current_alarm +5)

    elif(okita):
        status_csv_write("B", 1, 9999) # 起きたのでcsv書き換え

        ####################################################
        ##### I/O なし/実行終了合図      ######
        ##### うんちくずんだもん起動   ######
        ####################################################

        subprocess.run("echo 'standby 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
        print("TV off")

        status_csv_write("B", 2, 9999) # 起きたのでcsv書き換えて終了


# 外出中
elif current_status == 'B' and times == 2 and current_alarm == 9999:

    camera.take_photo() # take photo
    # check goout/inhome
    if BrightnessChecker.homeChecker():
        # true -> in home
        subprocess.run("echo 'on 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
        print("TV on")


        # rec.recording()
        ####################################################
        ##### I/O なし/実行終了      ######
        ##### 起床時間設定プログラム起動  ######
        ####################################################
        url = "http://127.0.0.1:8000/api/mp3_openai/"
        response = requests.post(url)
        
        response_line = int(response.json()['response'])
        set_alarm = int(response.json()['time'])
        status_csv_write("B", 3, set_alarm)

        subprocess.run("echo 'standby 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
        print("TV standby")

# 日付またぎ(アラーム時間と現在時間を大小比較するため)
elif current_status == 'B' and times == 3 and current_alarm == 9999:
    if "0000" <= current_time <= "0030": # 冗長
        status_csv_write("A", 0, current_alarm)
