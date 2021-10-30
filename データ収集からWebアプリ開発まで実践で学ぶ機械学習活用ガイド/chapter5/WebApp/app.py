# -*- coding: utf-8 -*-
from flask import Flask, render_template

# appという名前でFlaskオブジェクトをインスタンス化
app = Flask(__name__)

# rootディレクトリにアクセスした場合の挙動


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# メインで実行される関数
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
