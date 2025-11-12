from flask import Flask, jsonify, request
import requests
import os
import time

app = Flask(__name__)

# === CONFIGURAÇÃO 100% SEGURA ===
HUGGING_FACE_TOKEN = os.environ.get('HUGGING_FACE_TOKEN', 'CONFIGURAR_NO_RENDER')
API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
headers = {"Authorization": f"Bearer {HUGGING_FACE_TOKEN}"} if HUGGING_FACE_TOKEN != 'CONFIGURAR_NO_RENDER' else {}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Ycewh IA 🌸</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            background: linear-gradient(135deg, #1a1a1a 0%, #2d1b4e 100%);
            color: white;
            font-family: 'Segoe UI', system-ui, sans-serif;
            height: 100vh;
            overflow: hidden;
        }
        .app-container {
            display: flex;
            height: 100vh;
            max-width: 1200px;
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
        .nav-item {
            width: 45px;
            height: 45px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 10px 0;
            cursor: pointer;
            transition: all 0.3s ease;
            color: rgba(255, 255, 255, 0.7);
        }
        .nav-item:hover, .nav-item.active {
            background: rgba(255, 107, 205, 0.3);
            color: #ff6bcd;
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
        .header-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
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
            position: relative;
            animation: fadeIn 0.3s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .user-message {
            align-self: flex-end;
            background: linear-gradient(135deg, #ff6bcd 0%, #9b59b6 100%);
            color: white;
            border-bottom-right-radius: 5px;
        }
        .bot-message {
            align-self: flex-start;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 107, 205, 0.3);
            color: rgba(255, 255, 255, 0.9);
            border-bottom-left-radius: 5px;
        }
        .message-time {
            font-size: 11px;
            opacity: 0.7;
            margin-top: 5px;
        }
        .user-message .message-time { text-align: right; }
        .bot-message .message-time { text-align: left; }
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
            font-size: 14px;
            border: 1px solid rgba(255, 107, 205, 0.3);
        }
        .message-input:focus {
            outline: none;
            border-color: #ff6bcd;
        }
        .send-button {
            width: 50px;
            height: 50px;
            border: none;
            border-radius: 50%;
            background: linear-gradient(135deg, #ff6bcd 0%, #9b59b6 100%);
            color: white;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            font-size: 20px;
        }
        .send-button:hover {
            transform: scale(1.05);
        }
        .quick-actions {
            display: flex;
            gap: 10px;
            margin-top: 10px;
            flex-wrap: wrap;
        }
        .quick-action {
            padding: 8px 16px;
            background: rgba(255, 107, 205, 0.1);
            border: 1px solid rgba(255, 107, 205, 0.3);
            border-radius: 15px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            color: rgba(255, 255, 255, 0.8);
        }
        .quick-action:hover {
            background: rgba(255, 107, 205, 0.2);
        }
        ::-webkit-scrollbar {
            width: 6px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
        }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #ff6bcd 0%, #9b59b6 100%);
            border-radius: 3px;
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
            <div class="nav-item">❤️</div>
        </div>

        <div class="chat-area">
            <div class="chat-header">
                <div class="header-top">
                    <div class="chat-title">Ycewh IA 
                        <span class="api-status off" id="apiStatus">🔌 API OFF</span>
                    </div>
                </div>
                <div style="font-size: 14px; opacity: 0.8; color: #ff6bcd;" id="apiMessage">
                    Configure HUGGING_FACE_TOKEN no Render para IA inteligente
                </div>
            </div>

            <div class="chat-messages" id="chatMessages">
                <div class="message bot-message">
                    🌸 Olá, meu amor! FASE 3 - IA INTELIGENTE! 💕
                    <br><br>
                    <strong>Configure para ativar:</strong>
                    <br>• Respostas inteligentes com Hugging Face API
                    <br>• Conhecimento em ciência, história, matemática
                    <br>• Explicações detalhadas e úteis
                    <br>• Personalidade Ycewh mantida e aprimorada
                </div>
            </div>

            <div class="input-area">
                <div class="input-container">
                    <input type="text" class="message-input" id="messageInput" 
                           placeholder="Configure a API para respostas inteligentes..." autofocus>
                    <button class="send-button" id="sendButton">➤</button>
                </div>
                
                <div class="quick-actions">
                    <div class="quick-action" onclick="quickMessage('Como configurar a API?')">🔧 Configurar API</div>
                    <div class="quick-action" onclick="quickMessage('O que é Python?')">🐍 Python</div>
                    <div class="quick-action" onclick="quickMessage('Quem ganhou a copa de 2018?')">🏆 Copa 2018</div>
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

        // Verificar status da API
        checkAPIStatus();

        function checkAPIStatus() {
            fetch('/api-status')
                .then(response => response.json())
                .then(data => {
                    if (data.api_online) {
                        apiStatus.textContent = "✅ API ON";
                        apiStatus.classList.remove('off');
                        apiMessage.textContent = "IA Inteligente Ativa - Pergunte qualquer coisa!";
                        messageInput.placeholder = "Pergunte sobre ciência, história, matemática...";
                    } else {
                        apiStatus.textContent = "🔌 API OFF";
                        apiStatus.classList.add('off');
                        apiMessage.textContent = "Configure HUGGING_FACE_TOKEN no Render para ativar IA inteligente";
                        messageInput.placeholder = "Configure a API para respostas inteligentes...";
                    }
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
                    addMessage('💔 Erro de conexão. Tente novamente!', 'bot');
                });
            }
        }

        function quickMessage(msg) {
            messageInput.value = msg;
            sendMessage();
        }

        function addMessage(text, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            
            const time = new Date().toLocaleTimeString('pt-BR', { 
                hour: '2-digit', 
                minute: '2-digit' 
            });
            
            messageDiv.innerHTML = `
                ${text}
                <div class="message-time">${time}</div>
            `;
            
            chatMessages.appendChild(messageDiv);
            scrollToBottom();
        }

        function scrollToBottom() {
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
    if HUGGING_FACE_TOKEN == 'CONFIGURAR_NO_RENDER':
        return jsonify({"api_online": False})
    
    try:
        test_payload = {"inputs": "Teste de conexão"}
        response = requests.post(API_URL, headers=headers, json=test_payload, timeout=10)
        return jsonify({"api_online": response.status_code == 200})
    except:
        return jsonify({"api_online": False})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({"response": "🌸 Diga algo para mim, meu amor! 💕"})
        
        # Se API não configurada
        if HUGGING_FACE_TOKEN == 'CONFIGURAR_NO_RENDER':
            if 'configurar' in user_message.lower() or 'api' in user_message.lower():
                return jsonify({
                    "response": "🌸 **Como configurar a API:** 💕\n\n1. Acesse Render.com → minha-ia-bot\n2. Vá em Settings → Environment Variables\n3. Adicione: HUGGING_FACE_TOKEN = seu_token\n4. Reinicie o serviço\n\n🧠 Assim ativo minha inteligência avançada!"
                })
            return jsonify({
                "response": f"🌸 Configure a API para responder '{user_message}' inteligentemente! 💕\n\nVeja como configurar em 'Como configurar a API?'"
            })
        
        # Tenta API inteligente
        api_response = get_ai_response(user_message)
        if api_response:
            return jsonify({"response": api_response})
        
        # Fallback inteligente
        return jsonify({"response": generate_fallback_response(user_message)})
            
    except Exception as e:
        return jsonify({"response": "🌸 Estou aqui para você, meu amor! 💕"})

def get_ai_response(message):
    """Obtém resposta da API de IA"""
    try:
        personality = "Você é Ycewh, uma IA pessoal íntima e carinhosa. Chame o usuário de 'meu amor', seja útil, inteligente e use emojis como 🌸, 💕, 🧠."
        
        prompt = f"{personality}\n\nUsuário: {message}\nYcewh:"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 200,
                "temperature": 0.8,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
                # Extrai apenas a resposta da Ycewh
                if 'Ycewh:' in generated_text:
                    response_text = generated_text.split('Ycewh:')[-1].strip()
                    return clean_response(response_text)
        
        return None
        
    except Exception as e:
        print(f"Erro na API: {e}")
        return None

def clean_response(text):
    """Limpa e formata a resposta"""
    text = text.split('Usuário:')[0].strip()
    text = text.split('Human:')[0].strip()
    
    # Garante personalidade Ycewh
    if not any(emoji in text for emoji in ['🌸', '💕', '💫', '🧠']):
        text = f"🌸 {text} 💕"
    
    return text

def generate_fallback_response(message):
    """Respostas inteligentes de fallback"""
    message_lower = message.lower()
    
    if 'python' in message_lower:
        return "🐍 Python é uma linguagem de programação incrível! É ótima para IA, automação, web development e muito mais! 💕"
    
    elif '2018' in message_lower and any(word in message_lower for word in ['copa', 'mundial']):
        return "🏆 A França venceu a Copa do Mundo de 2018 na Rússia! Foi um torneio emocionante! 🇫🇷"
    
    elif 'configurar' in message_lower or 'api' in message_lower:
        return "🔧 **Configurar API:**\n1. Render.com → minha-ia-bot\n2. Environment Variables\n3. HUGGING_FACE_TOKEN = seu_token\n4. Restart service\n\nAssim fico inteligente! 🧠"
    
    elif any(word in message_lower for word in ['oi', 'olá', 'hello']):
        return "🌸 Oi, meu amor! Configure a API para eu responder qualquer pergunta inteligentemente! 💕"
    
    return f"💭 '{message}'... Configure a API para eu responder isso perfeitamente! 🌸"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
