from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
import os
from dotenv import load_dotenv


load_dotenv()

SLACK_API_KEY = os.getenv("SLACK_API_KEY")

client = WebClient(token=SLACK_API_KEY)


@api_view(['GET'])
def send_image_with_text(request):
    channel_id = "C07QE91Q6U9"
    message_text = "木村さんはまだ寝ています。"
    image_path = os.path.join(os.path.dirname(settings.BASE_DIR), "audio", "image.png")


    try:
        with open(image_path, 'rb') as file:
            response = client.files_upload_v2(
                channel=channel_id,
                file=file,
                initial_comment=message_text
            )
        return Response({"message": "画像とテキストが正常に送信されました。", "url": response["file"]["permalink"]})
    except SlackApiError as e:
        return Response({"error": e.response["error"]}, status=400)
    except FileNotFoundError:
        return Response({"error": "指定された画像ファイルが見つかりません。"}, status=400)




