from datetime import datetime, timezone
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google Calendar APIのスコープ（読み書き権限）
SCOPES = ["https://www.googleapis.com/auth/calendar"]
TOKEN_PATH=f"{os.path.dirname(os.path.abspath(__file__))}/token.json"
CRED_PATH=f"{os.path.dirname(os.path.abspath(__file__))}/credentials.json"

# google API認証
def get_calendar_service():
    creds = None
    # 既存のトークンファイルがあれば読み込む（トークンは認証情報を保存するためのもの）
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    # 有効な認証情報がない場合、再認証を実行
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # トークンの期限が切れている場合、リフレッシュ
            creds.refresh(Request())
        else:
            # 初回認証、もしくはトークンがない場合に認証フローを開始
            flow = InstalledAppFlow.from_client_secrets_file(CRED_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # 認証情報をtoken.jsonに保存して次回以降再利用できるようにする
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    # Google Calendar APIサービスのインスタンスを作成
    service = build("calendar", "v3", credentials=creds)
    return service

#カレンダーに予定登録
def register_event(summary:str, start:str, end:str):
    service=get_calendar_service()
    # イベントの詳細情報
    event = {
        'summary': summary,  # イベントのタイトル
        'start': {  # イベント開始日時（日本時間）
            'dateTime': start,
            'timeZone': 'Asia/Tokyo'
        },
        'end': {  # イベント終了日時（日本時間）
            'dateTime': end,
            'timeZone': 'Asia/Tokyo'
        },
    }
    # イベントをGoogleカレンダーに追加
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % created_event.get('htmlLink'))  # 作成したイベントのリンクを出力
    return "登録成功"
   
# カレンダーから情報取得
def get_events(start:str, end:str):
    service = get_calendar_service()
    # 今から1週間分のイベントを取得する
    #now = datetime.now().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start,
        timeMax=end,
        maxResults= 2,
        singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        print('イベントが取得できませんでした')
        return "イベントが取得できませんでした"
    for event in events:
        scedule = event['start'].get('dateTime', event['start'].get('date'))
        print(scedule, event['summary'])
    return events
