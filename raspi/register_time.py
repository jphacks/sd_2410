from dotenv import load_dotenv
import os
import openai
import json

load_dotenv()
OPEN_AI_API=os.environ.get("OPEN_AI_API")
openai.api_key = OPEN_AI_API

#仮の関数
def register_time(time:str):
    with open("time.txt", "w") as f:
        f.write(time)
    return


#call functionで呼び出される関数を説明
function_description={
    "name":"register_time",
    "description":"時間を登録する関数",
        "parameters": {
            "type": "object",
            "properties": {
                "morning_time": {
                    "type": "string",
                    "description": "起きる時間を数字４文字で出力。例:- 入力:６時半に起こして- 出力:0630"
                }
            },
        "required": ["morning_time"]
    }
}

#文字起こしされた文章
mojiokoshi = "8時29分に起こして"

response = openai.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
        {"role": "system", "content": "明日の朝起きる時間を登録します"},
        {"role": "user", "content": mojiokoshi}
    ],
  functions=[function_description],
  function_call={"name":"register_time"}
)

# ChatGPTの応答から関数呼び出しの情報を取得
message = response.choices[0].message
print(message.function_call.arguments)

# 関数がplay_animの場合、関数を実行
if message.function_call.name == "register_time":
    print("register_timeが選択されました")
    args = json.loads(message.function_call.arguments)
    result = register_time(args["morning_time"])

    # 関数の結果をChatGPTに送信して応答を作成
    follow_up_response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content":"起床時間の登録が完了しました"},
            {"role": "user", "content": mojiokoshi + "のだ口調で応答して"}
        ]
    )

    print(follow_up_response.choices[0].message.content)
