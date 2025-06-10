from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json
import os
from datetime import datetime

# Configuração da aplicação
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Configuração do SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Funções auxiliares para carregar dados
def load_empresas():
    try:
        with open('empresas.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def load_grupos():
    try:
        with open('grupos_whatsapp.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_empresas(empresas):
    with open('empresas.json', 'w', encoding='utf-8') as f:
        json.dump(empresas, f, ensure_ascii=False, indent=2)

def save_grupos(grupos):
    with open('grupos_whatsapp.json', 'w', encoding='utf-8') as f:
        json.dump(grupos, f, ensure_ascii=False, indent=2)

# Rotas principais
@app.route('/')
def dashboard():
    empresas = load_empresas()
    grupos = load_grupos()
    
    stats = {
        'total_empresas': len(empresas),
        'empresas_ativas': len([e for e in empresas if e.get('ativo', True)]),
        'total_grupos': len(grupos),
        'grupos_ativos': len([g for g in grupos if g.get('ativo', True)])
    }
    
    return render_template('dashboard.html', stats=stats)

@app.route('/empresas')
def empresas():
    return render_template('empresas.html')

@app.route('/grupos')
def grupos():
    return render_template('grupos.html')

@app.route('/operacoes')
def operacoes():
    return render_template('operacoes.html')

@app.route('/configuracoes')
def configuracoes():
    return render_template('configuracoes.html')

# APIs para empresas
@app.route('/api/empresas', methods=['GET'])
def api_get_empresas():
    return jsonify(load_empresas())

@app.route('/api/empresas', methods=['POST'])
def api_create_empresa():
    data = request.json
    empresas = load_empresas()
    
    # Validar código único
    if any(e['codigo'] == data['codigo'] for e in empresas):
        return jsonify({'error': 'Código já existe'}), 400
    
    empresas.append(data)
    save_empresas(empresas)
    return jsonify({'success': True})

@app.route('/api/empresas/<int:codigo>', methods=['PUT'])
def api_update_empresa(codigo):
    data = request.json
    empresas = load_empresas()
    
    for i, empresa in enumerate(empresas):
        if empresa['codigo'] == codigo:
            empresas[i] = data
            save_empresas(empresas)
            return jsonify({'success': True})
    
    return jsonify({'error': 'Empresa não encontrada'}), 404

@app.route('/api/empresas/<int:codigo>', methods=['DELETE'])
def api_delete_empresa(codigo):
    empresas = load_empresas()
    empresas = [e for e in empresas if e['codigo'] != codigo]
    save_empresas(empresas)
    return jsonify({'success': True})

# APIs para grupos
@app.route('/api/grupos', methods=['GET'])
def api_get_grupos():
    return jsonify(load_grupos())

@app.route('/api/grupos', methods=['POST'])
def api_create_grupo():
    data = request.json
    grupos = load_grupos()
    grupos.append(data)
    save_grupos(grupos)
    return jsonify({'success': True})

@app.route('/api/grupos/<int:index>', methods=['PUT'])
def api_update_grupo(index):
    data = request.json
    grupos = load_grupos()
    
    if 0 <= index < len(grupos):
        grupos[index] = data
        save_grupos(grupos)
        return jsonify({'success': True})
    
    return jsonify({'error': 'Grupo não encontrado'}), 404

@app.route('/api/grupos/<int:index>', methods=['DELETE'])
def api_delete_grupo(index):
    grupos = load_grupos()
    
    if 0 <= index < len(grupos):
        grupos.pop(index)
        save_grupos(grupos)
        return jsonify({'success': True})
    
    return jsonify({'error': 'Grupo não encontrado'}), 404

# APIs de operações (simuladas)
@app.route('/api/gerar-prints', methods=['POST'])
def api_gerar_prints():
    socketio.emit('log_message', {'message': '🖼️ Simulando geração de prints...', 'timestamp': datetime.now().strftime('%H:%M:%S')})
    socketio.emit('log_message', {'message': '✅ Prints gerados com sucesso (modo demo)', 'timestamp': datetime.now().strftime('%H:%M:%S')})
    return jsonify({'success': True, 'message': 'Prints gerados (modo demo)'})

@app.route('/api/enviar-whatsapp', methods=['POST'])
def api_enviar_whatsapp():
    socketio.emit('log_message', {'message': '📱 Simulando envio WhatsApp...', 'timestamp': datetime.now().strftime('%H:%M:%S')})
    socketio.emit('log_message', {'message': '✅ Mensagens enviadas com sucesso (modo demo)', 'timestamp': datetime.now().strftime('%H:%M:%S')})
    return jsonify({'success': True, 'message': 'WhatsApp enviado (modo demo)'})

@app.route('/api/processo-completo', methods=['POST'])
def api_processo_completo():
    socketio.emit('log_message', {'message': '🚀 Iniciando processo completo...', 'timestamp': datetime.now().strftime('%H:%M:%S')})
    socketio.emit('log_message', {'message': '🖼️ Gerando prints...', 'timestamp': datetime.now().strftime('%H:%M:%S')})
    socketio.emit('log_message', {'message': '📱 Enviando WhatsApp...', 'timestamp': datetime.now().strftime('%H:%M:%S')})
    socketio.emit('log_message', {'message': '✅ Processo completo finalizado (modo demo)', 'timestamp': datetime.now().strftime('%H:%M:%S')})
    return jsonify({'success': True, 'message': 'Processo completo executado (modo demo)'})

# WebSocket events
@socketio.on('connect')
def handle_connect():
    emit('log_message', {'message': '🔗 Cliente conectado ao sistema', 'timestamp': datetime.now().strftime('%H:%M:%S')})

@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')

if __name__ == '__main__':
    # Configurações para produção/desenvolvimento
    is_production = os.environ.get('FLASK_ENV') == 'production'
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    if is_production:
        print("🚀 Iniciando UPAUDIT em modo PRODUÇÃO (Demo)")
        print(f"📊 Sistema disponível na porta {port}")
        socketio.run(app, debug=False, host=host, port=port)
    else:
        print("🚀 Iniciando UPAUDIT - Modo Demo")
        print("📊 Dashboard disponível em: http://localhost:5000")
        print("⚠️ Modo demo ativo - operações simuladas")
        socketio.run(app, debug=True, host='0.0.0.0', port=5000) 