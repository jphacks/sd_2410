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
                        {"role": "system", "content": "あなたは怒らせたら怖いお母さんです.あなたは自分の子供を起こしています。"},
                        {"role": "user", "content": f"日本語で6段階中{times}段階目くらいの口調で子供を起こしてください。3段階目から男性口調で起こってください。「もうこれで{times}回おこしてるよ」みたいに起こしてください"}
                    ]
            )
            # OpenAIからのレスポンスを取得
            answer = completion.choices[0].message.content
            logger.error(f"times: ({times})")
            logger.error(f"answer: {str(answer.json())}")
            return JsonResponse({'answer': answer})
        except Exception as e:
            logger.error(f"Error in wake_up function: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
