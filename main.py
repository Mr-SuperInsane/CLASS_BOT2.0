from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, PostbackEvent
)
import datetime
from message import schedule, scope, kanji, brightstage, tesuto, file, event_c, information, feedback, change, change_time

app = Flask(__name__)

line_bot_api = LineBotApi('BL7KSFCMl1n82l2FTjd12SdXs1O9wS9zmzTRQDSVoKjssrgBdojh94pRRhRDo4lEeYqsAhsJXH9r4d39k5J71dLtaFlFM+B4jqxqCYWARsISf81w5SYkfg1IOChpESbWYG+LoXlo++t3ag2Pdwq6twdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4a7d64faa1fb0e1edf7eb2f7e6c92e94')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 曜日
    weekday = datetime.date.today().weekday()
    # 時間
    now_time = int(datetime.datetime.now().strftime('%H'))
    
    now_time += 9
    if now_time > 24:
        weekday += 1
        now_time -= 24

    #入力メッセージ受け取り
    message = event.message.text
    if message == '時間割':
        message_content = schedule(weekday, now_time)
        line_bot_api.reply_message(
            event.reply_token,
            messages=message_content
        )
    elif message == '範囲表':
        message_content = scope()
        line_bot_api.reply_message(
            event.reply_token,
            messages=message_content
        )
    elif message == '提出物':
        message_content = file()
        line_bot_api.reply_message(
            event.reply_token,
            messages=message_content
        )
    elif message == '行事予定':
        message_content = event_c()
        line_bot_api.reply_message(
            event.reply_token,
             messages=message_content
        )
    elif message == '使い方':
        message_content = information()
        line_bot_api.reply_message(
            event.reply_token,
            messages=message_content
        )
    elif message == '質問・機能追加':
        message_content = feedback()
        line_bot_api.reply_message(
            event.reply_token,
            messages=message_content
        )
    elif '@dev' in message:
        message_list = message.split(',')
        message_command = message_list[1]
        list_num = len(message_list)
        if message_command == '提出物':
            if list_num > 2:
                change(message_command, list_num, message_list)
                message = TextSendMessage(text='提出物を変更しました')
            else:
                message = TextSendMessage(text='エラー:情報が不足しているか形式に誤りがあります')
        elif message_command == '時間割':
            if list_num == 9:
                change_time(message_list)
                message = TextSendMessage(text='時間割を変更しました')
            else:
                message = TextSendMessage(text='エラー:情報が不足しているか形式に誤りがあります')

        line_bot_api.reply_message(
            event.reply_token,
            message
        )
        # elif message_command == '時間割リセット':
        #     if list_num == 2:
        #         reset_time()
        #     else:
        #         line_bot_api.reply_message(
        #             event.reply_token,
        #             TextSendMessage(text='エラー')
        #             )
            

@handler.add(PostbackEvent)
def postback(event):
    postback = event.postback.data
    #漢字
    if postback == 'kanji':
        message_content = kanji()
    elif postback == 'brightstage':
        message_content = brightstage()
    elif postback == 'tesuto':
        #テスト期間 ON/OFF
        active = 'false'
        if active == 'true':
            message_content = tesuto()
        elif active == 'false':
            message_content = TextSendMessage(text='現在はテスト期間ではありません')

    line_bot_api.reply_message(
        event.reply_token,
        messages=message_content
    )
            
if __name__ == "__main__":
    app.run()
'''
$env:FLASK_ENV = "development"
$env:FLASK_APP = "main"
flask run
'''