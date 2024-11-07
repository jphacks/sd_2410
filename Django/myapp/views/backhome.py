from django.shortcuts import render
from openai import OpenAI
from django.http import JsonResponse
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging
from django.http import JsonResponse
from .views import openai_api_view
from rest_framework.test import APIRequestFactory
# OPENAI_API_KEY = settings.OPENAI_API_KEY
logger = logging.getLogger('myapp')
# APIキーを設定
OPENAI_API_KEY = settings.OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)

@api_view(['GET', 'POST'])
def call_openai_api(request):
    # APIRequestFactoryを使って内部的にリクエストを作成
    factory = APIRequestFactory()
    api_request = factory.post('/api/openai-api/', {'prompt': 'お母さん口調で子供にお帰りみたいなことを言ってください'}, format='json')

    # 内部的にopenai_api_viewを呼び出し、レスポンスを取得
    response = openai_api_view(api_request)

    # レスポンスの結果をクライアントに返す
    return response
