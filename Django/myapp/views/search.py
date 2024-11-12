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

OPENAI_API_KEY = settings.OPENAI_API_KEY
SERP_API_KEY = settings.SERP_API_KEY

search_tool = SerpAPIWrapper(serpapi_api_key=SERP_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

@api_view(['GET', 'POST'])
def search(request):
    if request.method == 'POST':
        try:
            # JSONデータをパース
            data = json.loads(request.body)
            response = search_tool.run("今日は何の日？か１つ教えてください。")

            try:
                # OpenAI APIの呼び出し
                completion = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "あなたはお母さんで、朝息子への挨拶をする。ママみたいな口調で話して"},
                            {"role": "user", "content": f"以下を基に息子に声をかけて（ため口でお母さんみたいに）。内容は短めで:{response}"}
                        ]
                )
                # OpenAIからのレスポンスを取得
                answer = completion.choices[0].message.content
                return JsonResponse({'answer': answer})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
            return JsonResponse({'error': 'Prompt is required'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
