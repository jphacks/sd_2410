import speech_recognition as sr
import openai
#import pygame
import json
from datetime import datetime
import dotenv
import os
import sys
from time import sleep
import pandas as pd

from modules.google_calender_api import get_events, register_event
from modules.my_socket import socket_com # ソケット通信
from modules import rec    


def send_to_unity_and_wait(message, speaker_id=-1, times=-1):
    df = pd.read_csv('modules/speaker.csv')
    # speaker_id = df['speaker_id'].iloc[0]

    message = f"{times}:{speaker_id}:{message}"
    socket_com.start_client_sendString(message) 
    return socket_com.start_server_getString() # サーバー立てて文字取得まで待機

def speaker_csv_read(filename='modules/speaker.csv'):
    # CSVファイルの最初の1行だけを読み込む
    first_row = pd.read_csv(filename, nrows=1)
    
    # それぞれのカラムから値を取得
    speaker_id = first_row['speaker_id'].iloc[0]
    speaker_name = first_row['speaker_name'].iloc[0]
    speaker_mate = first_row['speaker_mate'].iloc[0]
    system_prompt = first_row['system_prompt'].iloc[0]
    return speaker_id, speaker_name, speaker_mate, system_prompt

# 環境変数設定
dotenv.load_dotenv()
OPEN_AI_API=os.environ.get("OPEN_AI_API")
openai.api_key = OPEN_AI_API

WAKE_WORD = ["おい", "ずん", "ずんたん", "ずんだ", "こはる", "小春", "たかぎ", "高木", "ジョイマン"] # 任意のウェイクワードに変更可能

get_function_description={
    "name":"get_events",
    "description":f"カレンダーを参照して予定を取得する,現在時刻は{datetime.now().isoformat()}",
        "parameters": {
            "type": "object",
            "properties": {
                "start": {
                    "type": "string",
                    "description": "予定を参照する日の始まり(例:2024-11-17T00:00:00+09:00)"
                },
                "end": {
                    "type": "string",
                    "description": "# 予定を参照する日の終わり(例:2024-11-17T23:59:59+09:00)"
                }
            },
        "required": ["start", "end"]
        }
    }

register_function_description={
    "name":"register_event",
    "description":f"予定を登録する,現在時刻は{datetime.now().isoformat()}",
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "登録する予定の内容"
                },
                "start":{
                    "type": "string",
                    "description": "予定の開始時間(例:2024-11-17T09:00:00+09:00)"
                },
                 "end":{
                    "type": "string",
                    "description": "予定の終了時間(例:2024-11-17T13:00:00+09:00)"
                }
            },
        "required": ["summary", "start", "end"]
    }
}

def get_openai_response(user_prompt, system_prompt, model="gpt-4o-mini"):
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content":f"{system_prompt}。100字以内"},
                {"role": "user", "content": user_prompt}
                ],
            functions=[get_function_description, register_function_description],
            function_call="auto"
        )
        # 応答テキストを抽出
        # ChatGPTの応答から関数呼び出しの情報を取得
        message = response.choices[0].message
        # 関数がget_eventsの場合、関数を実行
        if message.function_call is not None and message.function_call.name == "get_events":
            print("get_eventsが選択されました")
            # print(args.get(args.get("start"),args.get("end"))) # デバッグ用
            args = json.loads(message.function_call.arguments)
            result = get_events(args.get("start"),args.get("end"))
            # 関数の結果をChatGPTに送信して応答を作成
            follow_up_response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content":f"{system_prompt}。カレンダーへのリンクは応答に含めないでください。100字以内"},
                    {"role": "user", "content": user_prompt},
                    message,
                    {"role": "function", "name": "get_event", "content":json.dumps({"schedule": result})}
                ]
            )
            print(follow_up_response.choices[0].message.content)
            return follow_up_response.choices[0].message.content
        if message.function_call is not None and message.function_call.name == "register_event":
            print("register_eventが選択されました")
            args = json.loads(message.function_call.arguments)
            print(args.get("summary"),args.get("start"),args.get("end"))
            result = register_event(args.get("summary"),args.get("start"),args.get("end"))
            # 関数の結果をChatGPTに送信して応答を作成
            follow_up_response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content":f"{system_prompt}。100字以内"},
                    {"role": "user", "content": user_prompt},
                    message,
                    {"role": "function", "name": "get_event", "content":json.dumps({"schedule": result})}
                ]
            )
            print(follow_up_response.choices[0].message.content)
            return follow_up_response.choices[0].message.content
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI APIでエラーが発生しました エラー：{e}")
        return None


#Unityが無い環境はこっち使ってください
# #ここにLLMからの応答データを入れる
# def speak_zunda(text):
#     # 音声合成用クエリを作成
#     query_payload = {'text': text, 'speaker': 3}
#     query_res = requests.post("http://127.0.0.1:50021/audio_query", params=query_payload)
#     #query_res.raise_for_status()
#     audio_query = query_res.json()

#     # 音声合成を実行して音声データを生成
#     synthesis_res = requests.post(
#         "http://127.0.0.1:50021/synthesis", #ローカルでやるとき
#         params={'speaker': 3},
#         json=audio_query
#     )

#     #synthesis_res.raise_for_status()

#     # 音声ファイルを保存して再生(絶対パス)
#     with open("C:\\WorkPlace\\test\\test.wav", "wb") as f:
#         f.write(synthesis_res.content)
        
#     pygame.mixer.init()
#     pygame.mixer.music.load("C:\\WorkPlace\\test\\test.wav")
#     pygame.mixer.music.play()

def detect_wake_word():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    print("音声を取得しています...")

    speaker_id, speaker_name, speaker_mate, system_prompt = speaker_csv_read()
    wake_word_responce = "どうしたんだ？"
    if speaker_name == "Zundamon" and speaker_name == "Zundan":
        wake_word_responce = "どうしたのだ？"
    elif speaker_name == "Takagi":
        wake_word_responce = "どうした？"
    elif speaker_name == "koharu":
        wake_word_responce = "どうしたの？"
    elif speaker_name == "Ikemen":
        wake_word_responce = "どうした？"


    with microphone as source:
        audio = recognizer.listen(source)  # 音声を取得
    try:
        # Google Speech Recognition APIで音声をテキストに変換
        transcription = recognizer.recognize_google(audio,language='ja-JP')
        print(f"Recognized text: {transcription}")

        # ウェイクワードが音声に含まれているかをチェック
        if any(word in transcription for word in WAKE_WORD):
            print("ウェイクワードが検出されました！")
            # sys.exit(0) # 確認用

            send_to_unity_and_wait(wake_word_responce, speaker_id=speaker_id) # Unityに送信して待機
            rec.recording() # recordingスタート

            with sr.AudioFile("modules/voice.wav") as source:
                audio = recognizer.listen(source)  # 再度音声を取得
            user_prompt = recognizer.recognize_google(audio, language='ja-JP')
            print(f"Recognized text: {user_prompt}")

            # OpenAIからの応答を取得
            response = get_openai_response(user_prompt, system_prompt=system_prompt)
            if response:
                send_to_unity_and_wait(response, speaker_id=speaker_id)
            else:
                print("応答を取得できませんでした。")
            return True
        else:
            return False

    except sr.UnknownValueError:
        # 音声が理解できなかった場合
        print("音声を認識できませんでした")
        return False

    except sr.RequestError as e:
        # APIリクエストのエラー処理
        print(f"APIエラー")
        return False

while True:
    detect_wake_word()


