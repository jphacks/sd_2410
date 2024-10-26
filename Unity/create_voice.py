import requests
import json
import time

# ずんだもんの話者ID
speaker_id = 3

#ここにLLMからの応答データを入れる
text = """明日6時半に起こして"""

# 音声合成用クエリを作成
query_payload = {'text': text, 'speaker': speaker_id}
query_res = requests.post("http://127.0.0.1:50021/audio_query", params=query_payload)
query_res.raise_for_status()
audio_query = query_res.json()

# 音声合成を実行して音声データを生成
synthesis_res = requests.post(
    "http://127.0.0.1:50021/synthesis", #リクエスト投げるときはyotchiのPCのIPアドレスにしてください
    params={'speaker': speaker_id},
    json=audio_query
)
synthesis_res.raise_for_status()

# 音声ファイルを保存して再生
with open("zundamon_voice.wav", "wb") as f:
    f.write(synthesis_res.content)

print("音声ファイルが生成されました！")