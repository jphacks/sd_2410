import threading
import requests
from my_socket import socket_com
import subprocess
import camera
import time

def set_alarm(minutes):
    seconds = minutes * 60
    timer = threading.Timer(seconds, wake_me_up_in)
    timer.start()
    
def wake_me_up_in():
    okita = "0" # 初期化
    while(not(okita)):
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

            #TKD書き足し部分-スヌーズ機能用-----------------------
            url = f"http://127.0.0.1:8000/api/wake_up/{times}"
            response = requests.post(url)
            string = response.json().get('answer')
            #---------------------------------------------------
            socket_com.start_client_sendString(string) # サーバー接続して文字送信
            ####################################################
            ##### 起こすずんだもん起動   ######
            ####################################################
            socket_com.start_server_getString(65432) # サーバー立てて文字取得まで待機

            subprocess.run("echo 'standby 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
            print("TV off")
            
            time.sleep(300)
        
        elif(okita == "1"):
            print("起きたと判断")
            subprocess.run("echo 'on 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
            print("TV on")

            socket_com.start_client_sendString("今日8月20日はずんだ餅の日なのだ") # サーバー接続して文字送信
            ####################################################
            ##### I/O なし/実行終了合図      ######
            ##### うんちくずんだもん起動      ######
            ####################################################
            socket_com.start_server_getString(65432) # サーバー立てて文字取得まで待機

            subprocess.run("echo 'standby 0' | cec-client -s", shell=True, stdout=subprocess.DEVNULL)
            print("TV off")
    