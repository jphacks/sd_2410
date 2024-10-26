from django.shortcuts import render
from openai import OpenAI
from django.http import JsonResponse
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging

logger = logging.getLogger('myapp')
OPENAI_API_KEY = settings.OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)

@api_view(['POST'])
def mp3_view(request):
    if request.method == 'POST':
        try:
            data = request.data
            mp3file = data.get("filepath")
            audio_file= open(mp3file, "rb")
            transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
            return JsonResponse({'transcription': transcription.text})
        except Exception as e:
            # エラーログを記録し、エラーメッセージを返す
            logger.error(f"Error transcribing audio: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)