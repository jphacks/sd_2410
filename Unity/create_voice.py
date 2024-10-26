import requests
import json
import time

import sys
import os

# 親ディレクトリをPythonのパスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from sd_2410.audio.register_time import register_and_responce

# ずんだもんの話者ID
speaker_id = 3

#ここにLLMからの応答データを入れる
text = register_and_responce("6時43分に起こして")

# 音声合成用クエリを作成
query_payload = {'text': text, 'speaker': speaker_id}
query_res = requests.post("http://127.0.0.1:50021/audio_query", params=query_payload)
#query_res = requests.post("http://10.0.0.194:50021/audio_query", params=query_payload) #VPN接続して
query_res.raise_for_status()
audio_query = query_res.json()

# 音声合成を実行して音声データを生成
synthesis_res = requests.post(
    "http://127.0.0.1:50021/synthesis", #ローカルでやるとき
    params={'speaker': speaker_id},
    json=audio_query
)

# synthesis_res = requests.post(
#     "http://10.0.0.194:50021/synthesis", #リクエスト投げるときはyotchiのPCのIPアドレスにしてください
#     params={'speaker': speaker_id},
#     json=audio_query
# )

synthesis_res.raise_for_status()

# 音声ファイルを保存して再生
with open("sd_2410/Unity/Assets/zundamon_voice.wav", "wb") as f:
    f.write(synthesis_res.content)

print("音声ファイルが生成されました！")