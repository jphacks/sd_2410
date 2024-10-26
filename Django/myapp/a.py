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
from rest_framework.test import APIRequestFactory
logger = logging.getLogger('myapp')
OPENAI_API_KEY = settings.OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)
logger.info(OPENAI_API_KEY)

audio_file= open("C:/Users/17320/Downloads/zundamon_voice.wav", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)
print(transcription.text)