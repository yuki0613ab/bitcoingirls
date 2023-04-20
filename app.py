from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

# WebSocketを使用する場合
from flask_socketio import SocketIO

socketio = SocketIO(app)

# WebSocketイベントハンドラ
@socketio.on('connect')
def connect():
    print('connected')
    # ビットコイン価格の定期取得を開始
    update_price()

# ビットコイン価格の定期取得
def update_price():
    url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    response = requests.get(url)
    data = json.loads(response.text)
    price = data['bpi']['USD']['rate_float']
    # WebSocketでクライアントに通知
    socketio.emit('update', {'price': price})
    # 5秒毎に更新
    socketio.sleep(5)
    # 再帰的に呼び出し
    update_price()

# HTTPリクエストハンドラ
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app)
