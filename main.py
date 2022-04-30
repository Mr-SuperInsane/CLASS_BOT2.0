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
from message import change_bright, check_tesuto_onoff, schedule, scope, kanji, brightstage, tesuto, file, event_c, information, feedback, change_file, change_time,change_event,change_kanji,change_tesuto,change_tesuto_onoff

app = Flask(__name__)

line_bot_api = LineBotApi('チャンネルアクセストークン')
handler = WebhookHandler('シークレットトークン')


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
        now_time -= 24
        weekday += 1
        if weekday > 6:
            weekday = 0

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
                change_file(message_command, list_num, message_list)
                message = '提出物を変更しました'
            else:
                message = 'エラー:情報が不足しているか形式に誤りがあります'
        elif message_command == '時間割':
            if list_num == 9:
                change_time(message_list)
                message = '時間割を変更しました'
            else:
                message = 'エラー:情報が不足しているか形式に誤りがあります'

        elif message_command == '漢字':
            if list_num == 4:
                change_kanji(message_list)
                message = '漢字の範囲表を変更しました'
            else:
                message = 'エラー:情報が不足しているか形式に誤りがあります'

        elif message_command == 'ブライトステージ':
            if list_num == 4:
                change_bright(message_list)
                message = 'ブライトステージの範囲表を変更しました'
            else:
                message = 'エラー:情報が不足しているか形式に誤りがあります'

        elif message_command == 'テスト範囲':
            if list_num == 4:
                change_tesuto(message_list)
                message = '定期テストの範囲表を変更しました'
            else:
                message = 'エラー:情報が不足しているか形式に誤りがあります'

        elif message_command == '予定表':
            if list_num == 4:
                change_event(message_list)
                message = '予定表を変更しました'
            else:
                message = 'エラー:情報が不足しているか形式に誤りがあります'

        elif message_command == 'テスト':
            if list_num == 2:
                change_tesuto_onoff()
                active = check_tesuto_onoff()
                if active == '0':
                    message='定期テストをモードOFFにしました'
                elif active == '1':
                    message='定期テストをモードONにしました'
            else:
                message = 'エラー:情報が不足しているか形式に誤りがあります'
                
        elif message_command == 'ヘルプ':
            message = '''
【ベース】
　@dev,
【コマンド】
・時間割,曜日番号(1~5),1限,2限,3限,4限,5限,6限
・提出物,曜日:内容・・・
・漢字,URL(1024px),URL(240px)
・ブライトステージ,URL(1024px),URL(240px)
・予定表,URL(1024px),URL(240px)
・テスト範囲,URL(1024px),URL(240px)
・テスト
            '''

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )
            

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
        active = check_tesuto_onoff()
        if active == '1':
            message_content = tesuto()
        elif active == '0':
            message_content = TextSendMessage(text='現在はテスト期間ではありません')

    line_bot_api.reply_message(
        event.reply_token,
        messages=message_content
    )
            
if __name__ == "__main__":
    app.run(debug=True)
'''
$env:FLASK_ENV = "development"
$env:FLASK_APP = "main"
flask run
'''
