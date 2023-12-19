from flask import Flask
from datetime import datetime
from flask_cors import CORS #flaskにCORSを許可
import re
from flask_socketio import SocketIO, send, emit
from flask import Flask, render_template

# python -m flask run で動かす場合このファイルの名前は「app.py」か「wsgi.py」にする

app = Flask(__name__)
CORS(app) #flaskにCORSを許可
# Flaskの秘密鍵、実際の運用ではランダムかつ秘匿なものを使用してください
app.config['SECRET_KEY'] = 'secret!'

# cors_allowed_originは本来適切に設定するべき
socketio = SocketIO(app, cors_allowed_origins='*')

count = 0

@app.route('/')
def index():
    return render_template('index.html')  # 必要に応じてHTMLファイルをレンダリング

# WebSocket経由でクライアントが接続時に呼び出される
@socketio.on('connect')
def handle_connect():
    global count
    count += 1
    print('Client connected')
    # 接続されたクライアントに「hello, world」を送信
    socketio.emit('message', {'data': f'hello, world × {count}'})

# python -m flask run ではなくスタンドアロンで走らせたいならこれを書く（この際は任意のファイル名にできる）
if __name__ == "__main__":
    #runメソッドでビルトインサーバーが走る
    app.run()