import json
import time
from googleapiclient.discovery import build
from linebot import LineBotApi
from linebot.models import TextSendMessage

# info.jsonにAPIKEY等を記載
file = open('info.json','r')
info = json.load(file)
# YouTubeに関する設定
TARGET_CHANNEL_ID = info['TARGET_CHANNEL_ID']
YOUTUBE_API_KEY = info['YOUTUBE_API_KEY']
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
# 目標チャンネル登録者数
TARGET_SUBSCRIBER_COUNT = 100000
# LINE情報
CHANNEL_ACCESS_TOKEN = info['CHANNEL_ACCESS_TOKEN']
USER_ID = info['USER_ID']

def get_auth_service():
    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=YOUTUBE_API_KEY
    )
    return youtube

def get_subscriber_count(youtube):
    search_response = youtube.channels().list(
        part='statistics',
        id = TARGET_CHANNEL_ID,
    ).execute()
    return int(search_response['items'][0]['statistics']['subscriberCount'])

def main():
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    youtube = get_auth_service()
    
    while True:
        try:
            subscriber_count = get_subscriber_count(youtube)
            if subscriber_count >= TARGET_SUBSCRIBER_COUNT:
                messages = TextSendMessage(text='吉乃さんのチャンネル登録者数が100000人達成しました！')
                line_bot_api.push_message(USER_ID, messages=messages)
                break
            time.sleep(60)
        except Exception as e:
            error_messages = TextSendMessage(text=f'エラー発生：{e}')
            line_bot_api.push_message(USER_ID, messages=error_messages)
            time.sleep(60)

if __name__ == "__main__":
    main()