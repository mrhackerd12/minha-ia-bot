from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ycewh IA 🌸</title>
        <style>
            body { background: #1a1a1a; color: white; font-family: Arial; margin: 0; padding: 50px; text-align: center; }
            h1 { color: #ff6bcd; }
        </style>
    </head>
    <body>
        <h1>🌸 Ycewh IA 🌸</h1>
        <p><strong>VERIFICAÇÃO DE ESTADO</strong></p>
        <p>Git Status: ✅ Limpo</p>
        <p>Pronto para Fase 3!</p>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
