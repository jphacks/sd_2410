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

logger = logging.getLogger('myapp')
OPENAI_API_KEY = settings.OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)

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
            image_path = "C:/Users/17320/Downloads/image1.jpg"
            # Getting the base64 string
            base64_image = encode_image(image_path)
            response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": "この画像は何ですか?",
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
            )
            return response.choices[0]
            # return JsonResponse({'transcription': transcription.text})
        except Exception as e:
            # エラーログを記録し、エラーメッセージを返す
            logger.error(f"Error transcribing audio: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)