from django.shortcuts import render
from openai import OpenAI 
from django.http import JsonResponse
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging

from langchain_community.utilities import SerpAPIWrapper
import logging

# ロギングの設定
logger = logging.getLogger(__name__)

OPENAI_API_KEY = settings.OPENAI_API_KEY
SERP_API_KEY = settings.SERP_API_KEY

search_tool = SerpAPIWrapper(serpapi_api_key=SERP_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

@api_view(['POST'])
def wake_up(request, times):
    if request.method == 'POST':
        try:
            # OpenAI APIの呼び出し
            completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "あなたはお母さんです．あなたは自分の子供を起こしています．あなたには[0,1]の範囲の怒りポイントがあります．怒りポイントが1に近づくほど怒ってください．文字数は50文字程度"},
                        {"role": "user", "content": f"子供を起こしてください．今のあなたの怒りポイントは{times/6}です．{times}が1より大きい時は応答に「これで起こすのは{times}回目」という旨の情報をつけてください．"}
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
