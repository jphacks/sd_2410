from django.shortcuts import render
from openai import OpenAI
from django.http import JsonResponse
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging
import base64
import os

logger = logging.getLogger('myapp')
OPENAI_API_KEY = settings.OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)
description_message = {
    "role": "system",
    "content": (
        "以下のフォーマットで時間を入力してください。\n"
        "起きている場合は「０」"
        "出力例:0"
        "寝ている場合は「1」"
        "出力例:1"
    )
}
# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')



@api_view(['POST'])
def image_view(request):
    if request.method == 'POST':
        try:
            # data = request.data
            # mp3file = data.get("filepath")
            # audio_file= open(mp3file, "rb")
            # transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
            image_path = os.path.join(os.path.dirname(settings.BASE_DIR), "photo.jpg")
            # Getting the base64 string
            base64_image = encode_image(image_path)
            response = client.chat.completions.create(
            model="gpt-4o-mini",

            messages=[
                description_message,
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": "この画像に写っている人は起きていますか。起きている場合は1を、そうでない場合は0をjson形式で返してください。",
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url":  f"data:image/jpeg;base64,{base64_image}"
                    },
                    
                    },
                ],
                }
            ],
            response_format={"type": "json_object"}
            )
            print(response.choices[0].message.content)
            return Response(response.choices[0].message.content)
            # return JsonResponse({'transcription': transcription.text})
        except Exception as e:
            # エラーログを記録し、エラーメッセージを返す
            logger.error(f"Error transcribing audio: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)