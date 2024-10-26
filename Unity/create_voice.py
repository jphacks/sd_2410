import requests
import json
import time
from .socketServer import getString_socket

import sys
import os

# 親ディレクトリをPythonのパスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from sd_2410.audio.register_time import register_and_responce

# ずんだもんの話者ID
speaker_id = 3

#ここにLLMからの応答データを入れる
<<<<<<< HEAD
text = getString_socket()

=======
text = register_and_responce("6時43分に起こして")
print(text)
>>>>>>> 9f42f37e5a60c8d056f706204d529ca70c3b60b1
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
with open("sd_2410/Unity/Assets/resouce/zundamon_voice.wav", "wb") as f:
    f.write(synthesis_res.content)

# 文字ファイルを保存
with open("sd_2410/Unity/Assets/resouce/responce.txt", "w") as f:
    f.write(text)

print("音声・文字ファイルが生成されました！")