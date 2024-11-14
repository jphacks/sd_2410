import requests
import json
import time
import sys
import os

# 親ディレクトリをPythonのパスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from sd_2410.Unity.socket_server import getString_socket

wav_path = "C:/Users/renta/Joyman/Assets/Audio/"
text_path = "C:/Users/renta/Joyman/Assets/Text/responce.txt"

is_test_with_no_voicevox = True #voicevoxがないPCでテストするか

# ずんだもんの話者ID
speaker_id = 3
#speaker_id = 67
while 1:
    #ここにLLMからの応答データを入れる
    socket_get_data = getString_socket()

    num = None
    if socket_get_data[0].isdigit():
        num, text = socket_get_data.split(":") 
    else :
        text = socket_get_data
    
    if is_test_with_no_voicevox:
        print(text)
    else:
        # 音声合成用クエリを作成
        query_payload = {'text': text, 'speaker': speaker_id}
        query_res = requests.post("http://127.0.0.1:50021/audio_query", params=query_payload)
        query_res.raise_for_status()
        audio_query = query_res.json()

        # 音声合成を実行して音声データを生成
        synthesis_res = requests.post(
            "http://127.0.0.1:50021/synthesis", #ローカルでやるとき
            params={'speaker': speaker_id},
            json=audio_query
        )

        file_name = "bando.wav" if num=="1" else "abando.wav"   # ファイル名に直接.wavを書いた

        synthesis_res.raise_for_status()

        # 音声ファイルを保存して再生(絶対パス)
        with open(wav_path + file_name, "wb") as f:
            f.write(synthesis_res.content)

        # 文字ファイルを保存(絶対パス)
        with open(text_path, "w",encoding="utf-8") as f:
            f.write(text)

    print("音声・文字ファイルが生成されました！")


# def create_voice(text):
#     #ここにLLMからの応答データを入れる
#     #text = "おはようございますですわ"

#     # 音声合成用クエリを作成
#     query_payload = {'text': text, 'speaker': speaker_id}
#     query_res = requests.post("http://127.0.0.1:50021/audio_query", params=query_payload)
#     query_res.raise_for_status()
#     audio_query = query_res.json()

#     # 音声合成を実行して音声データを生成
#     synthesis_res = requests.post(
#         "http://127.0.0.1:50021/synthesis", #ローカルでやるとき
#         params={'speaker': speaker_id},
#         json=audio_query
#     )

#     synthesis_res.raise_for_status()

#     # 音声ファイルを保存して再生(絶対パス)
#     with open("C:/Users/renta/Joyman/Assets/Audio/abando.wav", "wb") as f:
#         f.write(synthesis_res.content)

#     # 文字ファイルを保存(絶対パス)
#     with open("C:/Users/renta/Joyman/Assets/Text/responce.txt", "w",encoding="utf-8") as f:
#         f.write(text)

#     print("音声・文字ファイルが生成されました！")