from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
from flask_socketio import SocketIO, emit
import json
import os
import threading
import time
from datetime import datetime, timedelta
from central_audit import (
    gerar_prints, enviar_whatsapp, get_empresas_ativas, 
    get_total_empresas, get_status_sistema, initialize_system
)
import logging
from pathlib import Path

# Configuração da aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'audit_system_2024_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Arquivos de dados
EMPRESAS_FILE = 'empresas.json'
GRUPOS_WHATSAPP_FILE = 'grupos_whatsapp.json'
CONFIG_FILE = 'config.json'

# Variáveis globais para controle de processos
current_process = None
process_status = {
    'running': False,
    'type': None,
    'progress': 0,
    'current_empresa': '',
    'total_empresas': 0,
    'sucessos': 0,
    'falhas': 0,
    'logs': []
}

def load_empresas():
    """Carrega lista de empresas do arquivo JSON"""
    if not os.path.exists(EMPRESAS_FILE):
        return []
    try:
        with open(EMPRESAS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Erro ao carregar empresas: {e}")
        return []

def save_empresas(empresas):
    """Salva lista de empresas no arquivo JSON"""
    try:
        with open(EMPRESAS_FILE, 'w', encoding='utf-8') as f:
            json.dump(empresas, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar empresas: {e}")
        return False

def load_config():
    """Carrega configurações do sistema"""
    if not os.path.exists(CONFIG_FILE):
        return {}
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Erro ao carregar configurações: {e}")
        return {}

def load_grupos_whatsapp():
    """Carrega grupos do WhatsApp do arquivo JSON"""
    if not os.path.exists(GRUPOS_WHATSAPP_FILE):
        return []
    try:
        with open(GRUPOS_WHATSAPP_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Erro ao carregar grupos WhatsApp: {e}")
        return []

def save_grupos_whatsapp(grupos_data):
    """Salva grupos do WhatsApp no arquivo JSON"""
    try:
        with open(GRUPOS_WHATSAPP_FILE, 'w', encoding='utf-8') as f:
            json.dump(grupos_data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar grupos WhatsApp: {e}")
        return False

def get_dashboard_stats():
    """Obtém estatísticas para o dashboard"""
    empresas = load_empresas()
    grupos = load_grupos_whatsapp()
    
    total_empresas = len(empresas)
    empresas_ativas = len([e for e in empresas if e.get('ativo', True)])
    empresas_inativas = total_empresas - empresas_ativas
    
    # Conta grupos únicos
    grupos_unicos = set()
    grupos_ativos = 0
    
    for grupo in grupos:
        if isinstance(grupo, dict) and grupo.get('grupo'):
            grupos_unicos.add(grupo['grupo'])
            if grupo.get('ativo', True):
                grupos_ativos += 1
    
    total_grupos = len(grupos_unicos)
    
    # Estatísticas por categoria
    categorias = {}
    for empresa in empresas:
        grupo = empresa.get('grupo', 'Sem Categoria')
        if grupo not in categorias:
            categorias[grupo] = {'total': 0, 'ativas': 0}
        categorias[grupo]['total'] += 1
        if empresa.get('ativo', True):
            categorias[grupo]['ativas'] += 1
    
    return {
        'total_empresas': total_empresas,
        'empresas_ativas': empresas_ativas,
        'empresas_inativas': empresas_inativas,
        'total_grupos': total_grupos,
        'grupos_ativos': grupos_ativos,
        'categorias': categorias,
        'ultima_atualizacao': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    }

def progress_callback(current, total, empresa_nome):
    """Callback para atualizar progresso via WebSocket"""
    global process_status
    
    process_status['progress'] = int((current / total) * 100)
    process_status['current_empresa'] = empresa_nome
    process_status['total_empresas'] = total
    
    # Emite atualização via WebSocket
    socketio.emit('progress_update', {
        'progress': process_status['progress'],
        'current_empresa': empresa_nome,
        'current': current,
        'total': total,
        'type': process_status['type']
    })

def log_callback(message):
    """Callback para logs em tempo real"""
    global process_status
    
    timestamp = datetime.now().strftime('%H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    
    process_status['logs'].append(log_entry)
    
    # Mantém apenas os últimos 100 logs
    if len(process_status['logs']) > 100:
        process_status['logs'] = process_status['logs'][-100:]
    
    # Emite log via WebSocket
    socketio.emit('log_update', {
        'message': log_entry,
        'timestamp': timestamp
    })

@app.route('/')
def dashboard():
    """Página principal do dashboard"""
    stats = get_dashboard_stats()
    return render_template('dashboard.html', stats=stats)

@app.route('/empresas')
def empresas():
    """Página de gerenciamento de empresas"""
    empresas_list = load_empresas()
    return render_template('empresas.html', empresas=empresas_list)

@app.route('/grupos')
def grupos():
    """Página de gerenciamento de grupos WhatsApp"""
    grupos_list = load_grupos_whatsapp()
    return render_template('grupos.html', grupos=grupos_list)

@app.route('/operacoes')
def operacoes():
    """Página de operações (prints e WhatsApp)"""
    return render_template('operacoes.html')

@app.route('/configuracoes')
def configuracoes():
    """Página de configurações do sistema"""
    config = load_config()
    return render_template('configuracoes.html', config=config)

@app.route('/api/empresas', methods=['GET'])
def api_get_empresas():
    """API para obter lista de empresas"""
    empresas_list = load_empresas()
    return jsonify(empresas_list)

@app.route('/api/empresas', methods=['POST'])
def api_add_empresa():
    """API para adicionar nova empresa"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['codigo', 'nome', 'grupo']):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    empresas_list = load_empresas()
    
    # Verifica se código já existe
    if any(e['codigo'] == data['codigo'] for e in empresas_list):
        return jsonify({'error': 'Código já existe'}), 400
    
    nova_empresa = {
        'codigo': data['codigo'],
        'nome': data['nome'],
        'grupo': data['grupo'],
        'nome_arquivo': f"{data['codigo']} - {data['nome']}.png",
        'ativo': data.get('ativo', True)
    }
    
    empresas_list.append(nova_empresa)
    
    if save_empresas(empresas_list):
        return jsonify({'success': True, 'empresa': nova_empresa})
    else:
        return jsonify({'error': 'Erro ao salvar'}), 500

@app.route('/api/empresas/<int:codigo>', methods=['PUT'])
def api_update_empresa(codigo):
    """API para atualizar empresa"""
    data = request.get_json()
    empresas_list = load_empresas()
    
    for i, empresa in enumerate(empresas_list):
        if empresa['codigo'] == codigo:
            empresas_list[i].update(data)
            if save_empresas(empresas_list):
                return jsonify({'success': True, 'empresa': empresas_list[i]})
            else:
                return jsonify({'error': 'Erro ao salvar'}), 500
    
    return jsonify({'error': 'Empresa não encontrada'}), 404

@app.route('/api/empresas/<int:codigo>', methods=['DELETE'])
def api_delete_empresa(codigo):
    """API para deletar empresa"""
    empresas_list = load_empresas()
    
    empresas_list = [e for e in empresas_list if e['codigo'] != codigo]
    
    if save_empresas(empresas_list):
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Erro ao salvar'}), 500

@app.route('/api/gerar-prints', methods=['POST'])
def api_gerar_prints():
    """API para iniciar geração de prints"""
    global current_process, process_status
    
    if process_status['running']:
        return jsonify({'error': 'Processo já em execução'}), 400
    
    data = request.get_json()
    modo_invisivel = data.get('modo_invisivel', True)
    
    def run_prints():
        global process_status
        
        process_status = {
            'running': True,
            'type': 'prints',
            'progress': 0,
            'current_empresa': '',
            'total_empresas': 0,
            'sucessos': 0,
            'falhas': 0,
            'logs': []
        }
        
        try:
            log_callback("🚀 Iniciando geração de prints...")
            sucessos, falhas = gerar_prints(progress_callback, modo_invisivel)
            
            process_status['sucessos'] = len(sucessos)
            process_status['falhas'] = len(falhas)
            
            log_callback(f"✅ Processo concluído! Sucessos: {len(sucessos)}, Falhas: {len(falhas)}")
            
            # Emite conclusão via WebSocket
            socketio.emit('process_complete', {
                'type': 'prints',
                'sucessos': len(sucessos),
                'falhas': len(falhas),
                'detalhes_sucessos': sucessos,
                'detalhes_falhas': falhas
            })
            
        except Exception as e:
            log_callback(f"❌ Erro durante geração de prints: {str(e)}")
            socketio.emit('process_error', {
                'type': 'prints',
                'error': str(e)
            })
        finally:
            process_status['running'] = False
    
    current_process = threading.Thread(target=run_prints, daemon=True)
    current_process.start()
    
    return jsonify({'success': True, 'message': 'Geração de prints iniciada'})

@app.route('/api/enviar-whatsapp', methods=['POST'])
def api_enviar_whatsapp():
    """API para iniciar envio para WhatsApp"""
    global current_process, process_status
    
    if process_status['running']:
        return jsonify({'error': 'Processo já em execução'}), 400
    
    data = request.get_json()
    modo_invisivel = data.get('modo_invisivel', True)
    
    def run_whatsapp():
        global process_status
        
        process_status = {
            'running': True,
            'type': 'whatsapp',
            'progress': 0,
            'current_empresa': '',
            'total_empresas': 0,
            'sucessos': 0,
            'falhas': 0,
            'logs': []
        }
        
        try:
            log_callback("📱 Iniciando envio para WhatsApp...")
            sucessos, falhas = enviar_whatsapp(progress_callback, modo_invisivel)
            
            process_status['sucessos'] = len(sucessos)
            process_status['falhas'] = len(falhas)
            
            log_callback(f"✅ Processo concluído! Sucessos: {len(sucessos)}, Falhas: {len(falhas)}")
            
            # Emite conclusão via WebSocket
            socketio.emit('process_complete', {
                'type': 'whatsapp',
                'sucessos': len(sucessos),
                'falhas': len(falhas),
                'detalhes_sucessos': sucessos,
                'detalhes_falhas': falhas
            })
            
        except Exception as e:
            log_callback(f"❌ Erro durante envio WhatsApp: {str(e)}")
            socketio.emit('process_error', {
                'type': 'whatsapp',
                'error': str(e)
            })
        finally:
            process_status['running'] = False
    
    current_process = threading.Thread(target=run_whatsapp, daemon=True)
    current_process.start()
    
    return jsonify({'success': True, 'message': 'Envio para WhatsApp iniciado'})

@app.route('/api/executar-completo', methods=['POST'])
def api_executar_completo():
    """API para executar processo completo (prints + WhatsApp)"""
    global current_process, process_status
    
    if process_status['running']:
        return jsonify({'error': 'Processo já em execução'}), 400
    
    data = request.get_json()
    modo_invisivel = data.get('modo_invisivel', True)
    
    def run_completo():
        global process_status
        
        process_status = {
            'running': True,
            'type': 'completo',
            'progress': 0,
            'current_empresa': '',
            'total_empresas': 0,
            'sucessos': 0,
            'falhas': 0,
            'logs': []
        }
        
        try:
            # Primeira fase: Prints
            log_callback("🚀 Fase 1/2: Iniciando geração de prints...")
            sucessos_prints, falhas_prints = gerar_prints(progress_callback, modo_invisivel)
            
            log_callback(f"✅ Prints concluídos! Sucessos: {len(sucessos_prints)}, Falhas: {len(falhas_prints)}")
            
            # Segunda fase: WhatsApp
            log_callback("📱 Fase 2/2: Iniciando envio para WhatsApp...")
            sucessos_whats, falhas_whats = enviar_whatsapp(progress_callback, modo_invisivel)
            
            total_sucessos = len(sucessos_prints) + len(sucessos_whats)
            total_falhas = len(falhas_prints) + len(falhas_whats)
            
            process_status['sucessos'] = total_sucessos
            process_status['falhas'] = total_falhas
            
            log_callback(f"🎉 Processo completo finalizado!")
            log_callback(f"📊 Resumo Final:")
            log_callback(f"   • Prints - Sucessos: {len(sucessos_prints)}, Falhas: {len(falhas_prints)}")
            log_callback(f"   • WhatsApp - Sucessos: {len(sucessos_whats)}, Falhas: {len(falhas_whats)}")
            log_callback(f"   • Total - Sucessos: {total_sucessos}, Falhas: {total_falhas}")
            
            # Emite conclusão via WebSocket
            socketio.emit('process_complete', {
                'type': 'completo',
                'sucessos': total_sucessos,
                'falhas': total_falhas,
                'detalhes': {
                    'prints': {'sucessos': sucessos_prints, 'falhas': falhas_prints},
                    'whatsapp': {'sucessos': sucessos_whats, 'falhas': falhas_whats}
                }
            })
            
        except Exception as e:
            log_callback(f"❌ Erro durante processo completo: {str(e)}")
            socketio.emit('process_error', {
                'type': 'completo',
                'error': str(e)
            })
        finally:
            process_status['running'] = False
    
    current_process = threading.Thread(target=run_completo, daemon=True)
    current_process.start()
    
    return jsonify({'success': True, 'message': 'Processo completo iniciado'})

@app.route('/api/parar-processo', methods=['POST'])
def api_parar_processo():
    """API para parar processo em execução"""
    global process_status
    
    if not process_status['running']:
        return jsonify({'error': 'Nenhum processo em execução'}), 400
    
    # Aqui você implementaria a lógica para parar o processo
    # Por enquanto, apenas marca como não executando
    process_status['running'] = False
    log_callback("⏹️ Processo interrompido pelo usuário")
    
    socketio.emit('process_stopped', {
        'message': 'Processo interrompido pelo usuário'
    })
    
    return jsonify({'success': True, 'message': 'Processo interrompido'})

@app.route('/api/status')
def api_status():
    """API para obter status atual do sistema"""
    return jsonify(process_status)

@app.route('/api/dashboard-stats')
def api_dashboard_stats():
    """API para obter estatísticas do dashboard"""
    return jsonify(get_dashboard_stats())

# ==================== CRUD GRUPOS WHATSAPP ====================

@app.route('/api/grupos', methods=['GET'])
def api_get_grupos():
    """API para obter lista de grupos WhatsApp"""
    grupos_list = load_grupos_whatsapp()
    return jsonify(grupos_list)

@app.route('/api/grupos', methods=['POST'])
def api_add_grupo():
    """API para adicionar novo grupo WhatsApp"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['grupo', 'empresa', 'arquivo']):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    grupos_list = load_grupos_whatsapp()
    
    novo_grupo = {
        'grupo': data['grupo'],
        'empresa': data['empresa'],
        'arquivo': data['arquivo'],
        'ativo': data.get('ativo', True)
    }
    
    grupos_list.append(novo_grupo)
    
    if save_grupos_whatsapp(grupos_list):
        return jsonify({'success': True, 'grupo': novo_grupo})
    else:
        return jsonify({'error': 'Erro ao salvar'}), 500

@app.route('/api/grupos/<int:index>', methods=['PUT'])
def api_update_grupo(index):
    """API para atualizar grupo WhatsApp"""
    data = request.get_json()
    grupos_list = load_grupos_whatsapp()
    
    if 0 <= index < len(grupos_list):
        grupos_list[index].update(data)
        if save_grupos_whatsapp(grupos_list):
            return jsonify({'success': True, 'grupo': grupos_list[index]})
        else:
            return jsonify({'error': 'Erro ao salvar'}), 500
    
    return jsonify({'error': 'Grupo não encontrado'}), 404

@app.route('/api/grupos/<int:index>', methods=['DELETE'])
def api_delete_grupo(index):
    """API para deletar grupo WhatsApp"""
    grupos_list = load_grupos_whatsapp()
    
    if 0 <= index < len(grupos_list):
        grupos_list.pop(index)
        if save_grupos_whatsapp(grupos_list):
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Erro ao salvar'}), 500
    
    return jsonify({'error': 'Grupo não encontrado'}), 404

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Cliente conectado via WebSocket"""
    emit('connected', {'message': 'Conectado ao sistema de auditoria'})

@socketio.on('disconnect')
def handle_disconnect():
    """Cliente desconectado via WebSocket"""
    print('Cliente desconectado')

@socketio.on('request_status')
def handle_request_status():
    """Cliente solicitou status atual"""
    emit('status_update', process_status)

if __name__ == '__main__':
    # Inicializa sistema
    try:
        initialize_system()
        logger.info("Sistema inicializado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar sistema: {e}")
    
    # Configurações para produção/desenvolvimento
    import os
    
    # Detecta se está em produção
    is_production = os.environ.get('FLASK_ENV') == 'production'
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    if is_production:
        print("🚀 Iniciando UPAUDIT em modo PRODUÇÃO")
        print(f"📊 Sistema disponível na porta {port}")
        socketio.run(app, debug=False, host=host, port=port)
    else:
        print("🚀 Iniciando Sistema de Auditoria Web")
        print("📊 Dashboard disponível em: http://localhost:5000")
        print("🔧 Modo de desenvolvimento ativo")
        socketio.run(app, debug=True, host='0.0.0.0', port=5000)