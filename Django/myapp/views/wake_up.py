from django.shortcuts import render
from openai import OpenAI 
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view
import logging

from langchain_community.utilities import SerpAPIWrapper
import logging
import json

# ロギングの設定
logger = logging.getLogger(__name__)

OPENAI_API_KEY = settings.OPENAI_API_KEY
SERP_API_KEY = settings.SERP_API_KEY

search_tool = SerpAPIWrapper(serpapi_api_key=SERP_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

@api_view(['POST'])
def wake_up(request, times):
    if request.method == 'POST':

        data = json.loads(request.body)
        system_prompt = data.get("system_prompt")
        mate = data.get("mate")
        user_name = data.get("user_name")

        try:
            # OpenAI APIの呼び出し

            warning_prompt = ""
            if times == 5:
                warning_prompt = "また，「次起きていなかったら，みんなにまだ寝ていることバラしちゃうよ」という旨を入れて"

            completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": f"{system_prompt}．あなたには[0,1]の範囲の怒りポイントがあります．怒りポイントが1に近づくほど怒ってください．"},
                        {"role": "user", "content": f"{user_name}を起こしてください．{user_name}はあなたにとって{mate}です．今のあなたの怒りポイントは{times/6}です．{times}が1より大きい時は応答に「これで起こすのは{times}回目」という旨の情報をつけてください．{warning_prompt}．文字数は80文字程度"}
                    ]
            )
            # OpenAIからのレスポンスを取得
            answer = completion.choices[0].message.content
            # logger.error(f"times: ({times})")
            # logger.error(f"answer: {answer}")

            return JsonResponse({'answer': answer})
        except Exception as e:
            logger.error(f"Error in wake_up function: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
