# 3-2BOT_1.0

Procfileとrequirements.txtはHeroku用のファイルです。ローカル環境でテストする場合、下記のコマンドでライブラリはインストールしてください。

    $pip install -r requirements.txt
    
# チャンネルアクセストークンとシークレットトークン

main.pyの17行目,18行目にはLINE Messaging APIのチャンネルアクセストークンとシークレットトークンをそれぞれ入力してください。

## GCP

message.pyの10行目にはgcpのsheetsの鍵(json形式)のファイル名を入力してください。12行目には利用するシートのIDを入力してください。IDはURLにあります。「--/d/シートID/edit--」

# webhook URL

ローカル環境で実行する場合はngrokで5000番を開放しSSL化されたURLをLINE管理画面のwebhook URLに入力してください。URLの末に「/callback」と付けてください。サーバで運用するときはURLをwebhook URLに入力してください。こちらも同様に「/callback」と付け忘れないようにしてください。

