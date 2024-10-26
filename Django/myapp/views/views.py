from django.shortcuts import render
from openai import OpenAI
from django.http import JsonResponse
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging

# OPENAI_API_KEY = settings.OPENAI_API_KEY
logger = logging.getLogger('myapp')
# APIキーを設定
OPENAI_API_KEY = settings.OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)
logger.info(OPENAI_API_KEY)
@api_view(['GET', 'POST'])
def openai_api_view(request):
    if request.method == 'POST':
        try:
            # JSONデータをパース
            data = json.loads(request.body)
            prompt = data.get('prompt', '')
            logger.info(f"prompt: {prompt}")
            if prompt:
                try:
                    # OpenAI APIの呼び出し
                    completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    # OpenAIからのレスポンスを取得
                    answer = completion.choices[0].message.content
                    return JsonResponse({'answer': answer})
                except Exception as e:
                    return JsonResponse({'error': str(e)}, status=500)
            else:
                return JsonResponse({'error': 'Prompt is required'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

