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

@api_view(['GET'])
def welcome_back(request):
    try:
        # OpenAI APIの呼び出し
        completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "あなたはお母さんです．あなたの子供はすでに働いているかもしれません．50文字で返答して．"},
                    {"role": "user", "content": "子供が家に帰ってきました．「おかえり」のような短い言葉と，明日は何時に起きるのか聞いてください"}
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
