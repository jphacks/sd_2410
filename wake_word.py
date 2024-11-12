import speech_recognition as sr
import openai
#import pygame
import json
from datetime import datetime
import dotenv
import os
import sys

from Unity.google_calender_api import get_events, register_event
from Unity.create_voice import create_voice
from my_socket import socket_com # ソケット通信

# 環境変数設定
dotenv.load_dotenv()
OPEN_AI_API=os.environ.get("OPEN_AI_API")
openai.api_key = OPEN_AI_API

WAKE_WORD = "おい"  # 任意のウェイクワードに変更可能

get_function_description={
    "name":"get_events",
    "description":"カレンダーを参照して今日の予定を取得する",
        "parameters": {
            "type": "object",
            "properties": {
                "schedule": {
                    "type": "string",
                    "description": "直近の予定"
                }
            },
        "required": ["schedule"]
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

def get_openai_response(prompt, model="gpt-4o-mini"):
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content":"生意気な口調で「なのだ」口調でしゃべって。100字以内"},
                {"role": "user", "content": prompt}
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
            #args = json.loads(message.function_call.arguments)
            result = get_events()
            # 関数の結果をChatGPTに送信して応答を作成
            follow_up_response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content":"生意気な口調で「なのだ」口調でしゃべって。カレンダーへのリンクは応答に含めないでください。100字以内"},
                    {"role": "user", "content": prompt},
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
                    {"role": "system", "content":"生意気な口調で「なのだ」口調でしゃべって。100字以内"},
                    {"role": "user", "content": prompt},
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

    with microphone as source:
        audio = recognizer.listen(source)  # 音声を取得
    try:
        # Google Speech Recognition APIで音声をテキストに変換
        transcription = recognizer.recognize_google(audio,language='ja-JP')
        print(f"Recognized text: {transcription}")

        # ウェイクワードが音声に含まれているかをチェック
        if WAKE_WORD in transcription:
            print("ウェイクワードが検出されました！")
            # sys.exit(0) # 確認用

            # 音声ファイルを保存して再生(絶対パス)
            # コピー元ファイルをバイナリで読み込み、コピー先ファイルに書き込む
            # with open( "sd_2410/first_response.wav", "rb") as src_file:
            #     data = src_file.read()
            # with open("C:/Users/renta/Joyman/Assets/Audio/abando.wav", "wb") as dest_file:
            #     dest_file.write(data)
            #     # 文字ファイルを保存(絶対パス)
            # with open("C:/Users/renta/Joyman/Assets/Text/responce.txt", "w",encoding="utf-8") as f:
            #     f.write("どうしたのだ？")

            remove_str=WAKE_WORD
            transcription = transcription.replace(remove_str, "")
            user_prompt = transcription

            # OpenAIからの応答を取得
            response = get_openai_response(user_prompt)
            if response:
                # create_voice(response) # unity PCで行うため以下に置き換え
                socket_com.start_client_sendString(response)
                ##############################################################
                ########            ソケット通信            ################
                ##############################################################
                socket_com.start_server_getString(65432)
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


