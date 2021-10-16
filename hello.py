from flask import Flask
from datetime import datetime
from flask_cors import CORS #flaskにCORSを許可
import re

# python -m flask run で動かす場合このファイルの名前は「app.py」か「wsgi.py」にする

app = Flask(__name__)
CORS(app) #flaskにCORSを許可

# Filter the "string" argument to letters only using regular expressions. URL arguments
# can contain arbitrary text, so we restrict to safe characters only.
def strfilter(string):
    match_object = re.match("[a-zA-Z0-9]+", string)
    if match_object:
        cleaned = match_object.group(0)
    else:
        cleaned = "Friend"
    return cleaned

@app.route("/")
# ※複数のパスを指定可能
#末尾のスラッシュの振る舞い
#1.
#このとき"/home/"を指定すると404
@app.route("/home")
def home():
    return "Flask Home"

#2.
#こうすれば"/hello/"でも"/hello"でもどちらでもいける（"/hello"は自動的に"/hello/"にリダイレクトされる）
#1.2.の振る舞いによって検索エンジンのクローラーが同じページに2回インデックスを付けることを回避している
@app.route('/hello/')
def hello():
    hello = "Hello world"
    return hello

#3.
#スラッシュあり/なしを両方有効にし
#かつ、スラッシュなしを自動的にスラッシュありにリダイレクトさせたくないときは
#この順番で記述する（逆に書くとなぜか"/hello2"が"/hello2/"にリダイレクトされる）
@app.route('/hello2/')
@app.route('/hello2')
def hello2():
    hello= "Good evening"
    return hello

# name を引数として受け取れる
@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    # name を安全な文字列に変換
    clean_name = strfilter(name)
    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content

# python -m flask run ではなくスタンドアロンで走らせたいならこれを書く（この際は任意のファイル名にできる）
if __name__ == "__main__":
    #runメソッドでビルトインサーバーが走る
    app.run()