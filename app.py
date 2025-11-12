from flask import Flask, jsonify, request
import requests
import os
import time

app = Flask(__name__)

# === CONFIGURAÇÃO COM DEBUG ===
HUGGING_FACE_TOKEN = os.environ.get('HUGGING_FACE_TOKEN')
print(f"🎯 DEBUG 1: Token carregado - {HUGGING_FACE_TOKEN is not None}")
print(f"🎯 DEBUG 2: Token valor - {HUGGING_FACE_TOKEN}")

API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
headers = {"Authorization": f"Bearer {HUGGING_FACE_TOKEN}"} if HUGGING_FACE_TOKEN else {}

print(f"🎯 DEBUG 3: Headers configurados - {bool(headers)}")

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Ycewh IA 🌸</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #1a1a1a 0%, #2d1b4e 100%);
            color: white;
            font-family: 'Segoe UI', sans-serif;
            height: 100vh;
            overflow: hidden;
        }
        .app-container {
            display: flex;
            height: 100vh;
            margin: 0 auto;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(20px);
        }
        .sidebar {
            width: 80px;
            background: rgba(255, 107, 205, 0.1);
            border-right: 1px solid rgba(255, 107, 205, 0.3);
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px 0;
        }
        .avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: linear-gradient(135deg, #ff6bcd 0%, #9b59b6 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            margin-bottom: 30px;
            border: 2px solid rgba(255, 255, 255, 0.3);
        }
        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        .chat-header {
            padding: 20px 30px;
            border-bottom: 1px solid rgba(255, 107, 205, 0.2);
            background: rgba(26, 26, 26, 0.9);
        }
        .chat-title {
            font-size: 24px;
            font-weight: 700;
            background: linear-gradient(135deg, #ff6bcd 0%, #9b59b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .api-status {
            background: rgba(76, 175, 80, 0.2);
            border: 1px solid rgba(76, 175, 80, 0.5);
            border-radius: 15px;
            padding: 5px 10px;
            font-size: 11px;
            margin-left: 10px;
        }
        .api-status.off {
            background: rgba(244, 67, 54, 0.2);
            border-color: rgba(244, 67, 54, 0.5);
        }
        .chat-messages {
            flex: 1;
            padding: 20px 30px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .message {
            max-width: 70%;
            padding: 15px 20px;
            border-radius: 20px;
            animation: fadeIn 0.3s ease;
        }
        .user-message {
            align-self: flex-end;
            background: linear-gradient(135deg, #ff6bcd 0%, #9b59b6 100%);
            color: white;
        }
        .bot-message {
            align-self: flex-start;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 107, 205, 0.3);
            color: rgba(255, 255, 255, 0.9);
        }
        .input-area {
            padding: 20px 30px;
            border-top: 1px solid rgba(255, 107, 205, 0.2);
            background: rgba(26, 26, 26, 0.9);
        }
        .input-container {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        .message-input {
            flex: 1;
            padding: 15px 20px;
            border: none;
            border-radius: 25px;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 107, 205, 0.3);
        }
        .send-button {
            width: 50px;
            height: 50px;
            border: none;
            border-radius: 50%;
            background: linear-gradient(135deg, #ff6bcd 0%, #9b59b6 100%);
            color: white;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="app-container">
        <div class="sidebar">
            <div class="avatar">🌸</div>
            <div class="nav-item active">💬</div>
            <div class="nav-item">🛠️</div>
            <div class="nav-item">⚙️</div>
        </div>

        <div class="chat-area">
            <div class="chat-header">
                <div class="header-top">
                    <div class="chat-title">Ycewh IA 
                        <span class="api-status off" id="apiStatus">🔌 API OFF</span>
                    </div>
                </div>
                <div style="font-size: 14px; opacity: 0.8; color: #ff6bcd;" id="apiMessage">
                    Configure HUGGING_FACE_TOKEN no Render
                </div>
            </div>

            <div class="chat-messages" id="chatMessages">
                <div class="message bot-message">
                    🌸 Olá! FASE 3 - IA INTELIGENTE! 💕
                    <br>Configure a API para respostas inteligentes
                </div>
            </div>

            <div class="input-area">
                <div class="input-container">
                    <input type="text" class="message-input" id="messageInput" 
                           placeholder="Configure a API..." autofocus>
                    <button class="send-button" id="sendButton">➤</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        const chatMessages = document.getElementById('chatMessages');
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');
        const apiStatus = document.getElementById('apiStatus');
        const apiMessage = document.getElementById('apiMessage');

        checkAPIStatus();

        function checkAPIStatus() {
            fetch('/api-status')
                .then(response => response.json())
                .then(data => {
                    if (data.api_online) {
                        apiStatus.textContent = "✅ API ON";
                        apiStatus.classList.remove('off');
                        apiMessage.textContent = "IA Inteligente Ativa!";
                        messageInput.placeholder = "Pergunte anything...";
                    }
                })
                .catch(error => {
                    console.error('Erro API:', error);
                });
        }

        function sendMessage() {
            const message = messageInput.value.trim();
            if (message) {
                addMessage(message, 'user');
                messageInput.value = '';
                
                fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message})
                })
                .then(response => response.json())
                .then(data => {
                    addMessage(data.response, 'bot');
                    checkAPIStatus();
                })
                .catch(error => {
                    addMessage('💔 Erro de conexão', 'bot');
                });
            }
        }

        function addMessage(text, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            messageDiv.innerHTML = text;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        sendButton.addEventListener('click', sendMessage);
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML

@app.route('/api-status')
def api_status():
    """Verifica status da API"""
    print(f"🎯 DEBUG 4: /api-status chamado - Token: {HUGGING_FACE_TOKEN is not None}")
    
    if not HUGGING_FACE_TOKEN:
        print("❌ DEBUG 5: Token NÃO encontrado!")
        return jsonify({"api_online": False})
    
    try:
        print("🎯 DEBUG 6: Testando conexão com Hugging Face...")
        test_payload = {"inputs": "Hello"}
        response = requests.post(API_URL, headers=headers, json=test_payload, timeout=10)
        print(f"🎯 DEBUG 7: Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ DEBUG 8: API ONLINE!")
        else:
            print(f"❌ DEBUG 9: API erro - Status: {response.status_code}")
            
        return jsonify({"api_online": response.status_code == 200})
        
    except Exception as e:
        print(f"❌ DEBUG 10: Exception: {e}")
        return jsonify({"api_online": False})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        print(f"🎯 DEBUG 11: Chat mensagem: {user_message}")
        
        if not HUGGING_FACE_TOKEN:
            return jsonify({"response": "🌸 Configure HUGGING_FACE_TOKEN no Render! 💕"})
        
        return jsonify({"response": f"🌸 TESTE: {user_message} - API funcionando! 💕"})
            
    except Exception as e:
        print(f"💥 DEBUG 12: Erro chat: {e}")
        return jsonify({"response": "🌸 Estou aqui para você! 💕"})

if __name__ == '__main__':
    print("🎯 SERVIDOR INICIANDO...")
    app.run(host='0.0.0.0', port=8080, debug=False)
