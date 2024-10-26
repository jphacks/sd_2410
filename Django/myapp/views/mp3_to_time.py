from django.shortcuts import render
from openai import OpenAI
from django.http import JsonResponse
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging
import os

logger = logging.getLogger('myapp')
OPENAI_API_KEY = settings.OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)

description_message = {
    "role": "system",
    "content": (
        "以下のフォーマットで時間を入力してください。\n"
        "6030"
        "起きる時間を4桁の数字で出力してください。例: 0630 （6時30分に起きる場合）"
    )
}

@api_view(['POST'])
def mp3_to_time(request):
    if request.method == 'POST':
        try:

            file_path = os.path.join(os.path.dirname(settings.BASE_DIR), "audio", "voice.wav")

            audio_file= open(file_path, "rb")
            transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
            # return JsonResponse({'transcription': transcription.text})
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    description_message,
                    {"role": "user", "content": transcription.text}
                ]
            )
            return Response(response.choices[0].message.content)

        except Exception as e:
            # エラーログを記録し、エラーメッセージを返す
            logger.error(f"Error transcribing audio: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)