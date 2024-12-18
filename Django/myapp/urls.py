from django.urls import path
from .views.image import image_view
from .views.mp3_to_time import mp3_to_time
from .views.okaeri import call_openai_api
from .views.search import search
from .views.send_image import send_image_with_text
from .views.sleep_remind import sleep_remind
from .views.views import openai_api_view  # 必要に応じてビューをインポート
from .views.wake_up import wake_up
from .views.welcome_back import welcome_back

# URL, importした関数名, メモ
urlpatterns = [
    path('openai-api/', openai_api_view, name='openai_api'),
    path('call_openai/', call_openai_api, name='call_openai_api'),
    path('mp3_openai/', mp3_to_time, name="mp3_api"),
    path('image_openai/', image_view, name="image_view"),
    path('search/', search, name="search_today"),
    path('send_image/', send_image_with_text, name='send_image'),
    path('wake_up/<int:times>/', wake_up, name='wake_up'),
    path('sleep_remind/', sleep_remind, name='sleep_remind'),
    path('welcome_back/', welcome_back, name='welcome_back')
]