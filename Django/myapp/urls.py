from django.urls import path
from .views.okaeri import call_openai_api
from .views.views import openai_api_view  # 必要に応じてビューをインポート
from .views.mp3_to_time import mp3_to_time
from .views.image import image_view
from .views.search import search
from .views.send_image import send_image_with_text
from .views.sleep_remind import sleep_remind

urlpatterns = [
    path('openai-api/', openai_api_view, name='openai_api'),
    path('call_openai/', call_openai_api, name='call_openai_api'),
    path('mp3_openai/', mp3_to_time, name="mp3_api"),
    path('image_openai/', image_view, name="image_view"),
    path('search/', search, name="image_view"),
    path('send_image/', send_image_with_text, name='send_image'),
    path('sleep_remind/', sleep_remind, name='sleep_remind')
]