import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>UPAUDIT - Sistema Online</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #1a365d; color: white; }
            .container { max-width: 600px; margin: 0 auto; }
            h1 { color: #00d4ff; font-size: 3em; margin-bottom: 20px; }
            p { font-size: 1.2em; margin: 20px 0; }
            .status { background: #4a90e2; padding: 20px; border-radius: 10px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 UPAUDIT</h1>
            <div class="status">
                <h2>✅ Sistema Online!</h2>
                <p>Deploy realizado com sucesso no Railway</p>
                <p>Versão de teste funcionando perfeitamente</p>
            </div>
            <p>🎉 Parabéns! O sistema está funcionando na nuvem!</p>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    """Rota de healthcheck para o Railway"""
    return {'status': 'ok', 'message': 'UPAUDIT funcionando!'}, 200

@app.route('/ping')
def ping():
    """Rota alternativa de healthcheck"""
    return 'pong', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 