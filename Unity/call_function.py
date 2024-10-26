from dotenv import load_dotenv
import os
import openai
import json

load_dotenv()
OPEN_AI_API=os.environ.get("OPEN_AI_API")
openai.api_key = OPEN_AI_API

#仮の関数
def play_anim(anim_id:str):
    print(anim_id)
    return


#call functionで呼び出される関数を説明
function_description={
    "name":"play_anim",
    "description":"Unity上のアニメーションを実行する",
        "parameters": {
            "type": "object",
            "properties": {
                "anim_id": {
                    "type": "string",
                    "description": """Unity上で実行されるアニメーションID {嬉しい:grad, 悲しい:sad, 怒り:angry}"""
                }
            },
        "required": ["anim_id"]
    }
}


response = openai.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
        {"role": "system", "content": "入力されてた文章から感情を読み取り、適切なアニメーションIDを選択します"},
        {"role": "user", "content": "いい加減起きなさい"}
    ],
  functions=[function_description],
  function_call={"name":"play_anim"}
)

# ChatGPTの応答から関数呼び出しの情報を取得
message = response.choices[0].message
print(message.function_call.arguments)

# 関数がplay_animの場合、関数を実行
if message.function_call.name == "play_anim":
    print("play_animが選択されました")
    args = json.loads(message.function_call.arguments)
    result = play_anim(args["anim_id"])

    # # 関数の結果をChatGPTに送信して応答を作成
    # follow_up_response = openai.ChatCompletion.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {"role": "user", "content": "東京の天気を教えてください。"},
    #         message,
    #         {"role": "function", "name": "get_weather", "content": json.dumps(result)}
    #     ]
    # )

    # print(follow_up_response["choices"][0]["message"]["content"])
