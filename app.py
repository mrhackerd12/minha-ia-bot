from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

HUGGING_FACE_TOKEN = os.environ.get('HUGGING_FACE_TOKEN', 'NAO_CONFIGURADO')

@app.route('/')
def home():
    return "Ycewh IA - Configure HUGGING_FACE_TOKEN no Render"

@app.route('/chat', methods=['POST'])
def chat():
    return jsonify({"response": "Configure a variável de ambiente"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
