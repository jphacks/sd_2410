from openai import OpenAI
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view
from langchain_community.utilities import SerpAPIWrapper
from rest_framework.response import Response

OPENAI_API_KEY = settings.OPENAI_API_KEY
SERP_API_KEY = settings.SERP_API_KEY

search_tool = SerpAPIWrapper(serpapi_api_key=SERP_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

@api_view(['GET'])
def sleep_remind(request):
    alarm_time = request.GET.get('alarm_time')
    sleep_duration = request.GET.get('sleep_duration')

    alarm_h = alarm_time[:2]
    alarm_m = alarm_time[2:]
    
    try:
        # OpenAI APIの呼び出し
        completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "あなたは，お母さんです．明日の朝起きられるように子供（成人）に睡眠の催促をしています，応答には100文字程度で答えてください．"},
                    {"role": "user", "content": f"子供に睡眠の催促をしてください．（例：明日{alarm_h}時{alarm_m}分に起きるには，そろそろ寝たほうがいいわよ．今眠ると{sleep_duration}時間も眠れるよ．）また，{sleep_duration}時間眠ることによるメリットも付け加えてください．"}
                ]
        )
        # OpenAIからのレスポンスを取得
        answer = completion.choices[0].message.content
        return JsonResponse({'answer': answer})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

