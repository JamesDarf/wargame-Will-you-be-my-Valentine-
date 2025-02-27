from flask import Flask, request, render_template, jsonify
from Crypto.Cipher import AES
import base64
import os

app = Flask(__name__, static_url_path='/static')

AES_KEY = "tha4nkUf0rcH0Co"

with open("flag.txt", "r") as f:
    FLAG = f.read().strip()

# AES 암호화 함수
def encrypt_data(data):
    cipher = AES.new(AES_KEY.encode(), AES.MODE_ECB)  # 취약한 ECB 모드 사용 (문제의 핵심)
    padded_data = data.ljust(16)  # 패딩 (블록 크기 맞춤)
    encrypted = cipher.encrypt(padded_data.encode())
    return base64.b64encode(encrypted).decode()


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')


@app.route("/yes", methods=["GET", "POST"])
def answer_yes():
    return render_template('yes_page.html')


# 암호화된 플래그 반환 API
@app.route("/api/secret", methods=["GET"])
def secret():
    encrypted_flag = encrypt_data(FLAG)
    return jsonify({"encrypted_flag": encrypted_flag})

if __name__ == "__main__":
    # 디버그 모드 활성화
    app.run(host="0.0.0.0", port=5000)
