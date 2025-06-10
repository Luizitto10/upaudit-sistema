import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_socketio import SocketIO, emit
import time
import threading

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicialização do Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '9225e5fe046b4e9eb11f276f751c9ed8072a34f0371f3deff0137ff6f4889174')

# Configuração do SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Variáveis globais
sistema_ativo = True
operacao_em_andamento = False

def log_sistema(mensagem, tipo="info"):
    """Função para logging com emissão via WebSocket"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {mensagem}"
    
    if tipo == "info":
        logger.info(mensagem)
        print(f"ℹ️ {log_entry}")
    elif tipo == "success":
        logger.info(mensagem)
        print(f"✅ {log_entry}")
    elif tipo == "warning":
        logger.warning(mensagem)
        print(f"⚠️ {log_entry}")
    elif tipo == "error":
        logger.error(mensagem)
        print(f"❌ {log_entry}")
    
    # Emitir via WebSocket
    socketio.emit('log_update', {
        'timestamp': timestamp,
        'message': mensagem,
        'type': tipo
    })

def carregar_empresas():
    """Carrega lista de empresas do arquivo JSON"""
    try:
        if os.path.exists('empresas.json'):
            with open('empresas.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        log_sistema(f"Erro ao carregar empresas: {str(e)}", "error")
        return []

def salvar_empresas(empresas):
    """Salva lista de empresas no arquivo JSON"""
    try:
        with open('empresas.json', 'w', encoding='utf-8') as f:
            json.dump(empresas, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        log_sistema(f"Erro ao salvar empresas: {str(e)}", "error")
        return False

def carregar_grupos():
    """Carrega lista de grupos WhatsApp do arquivo JSON"""
    try:
        if os.path.exists('grupos_whatsapp.json'):
            with open('grupos_whatsapp.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        log_sistema(f"Erro ao carregar grupos: {str(e)}", "error")
        return []

def salvar_grupos(grupos):
    """Salva lista de grupos WhatsApp no arquivo JSON"""
    try:
        with open('grupos_whatsapp.json', 'w', encoding='utf-8') as f:
            json.dump(grupos, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        log_sistema(f"Erro ao salvar grupos: {str(e)}", "error")
        return False

def obter_estatisticas():
    """Obtém estatísticas do sistema"""
    empresas = carregar_empresas()
    grupos = carregar_grupos()
    
    return {
        'total_empresas': len(empresas),
        'empresas_ativas': len([e for e in empresas if e.get('ativo', True)]),
        'total_grupos': len(grupos),
        'grupos_ativos': len([g for g in grupos if g.get('ativo', True)]),
        'sistema_status': 'online' if sistema_ativo else 'offline',
        'operacao_ativa': operacao_em_andamento
    }

# Rotas principais
@app.route('/')
def dashboard():
    """Página principal - Dashboard"""
    stats = obter_estatisticas()
    return render_template('dashboard.html', stats=stats)

@app.route('/operacoes')
def operacoes():
    """Página de operações"""
    return render_template('operacoes.html')

@app.route('/empresas')
def empresas():
    """Página de empresas"""
    empresas_list = carregar_empresas()
    return render_template('empresas.html', empresas=empresas_list)

@app.route('/grupos')
def grupos():
    """Página de grupos WhatsApp"""
    grupos_list = carregar_grupos()
    return render_template('grupos.html', grupos=grupos_list)

@app.route('/configuracoes')
def configuracoes():
    """Página de configurações"""
    return render_template('configuracoes.html')

# APIs REST para empresas
@app.route('/api/empresas', methods=['GET'])
def api_listar_empresas():
    """API para listar empresas"""
    empresas = carregar_empresas()
    return jsonify(empresas)

@app.route('/api/empresas', methods=['POST'])
def api_criar_empresa():
    """API para criar nova empresa"""
    try:
        dados = request.get_json()
        empresas = carregar_empresas()
        
        # Validar dados obrigatórios
        if not dados.get('codigo') or not dados.get('nome'):
            return jsonify({'error': 'Código e nome são obrigatórios'}), 400
        
        # Verificar se código já existe
        if any(e['codigo'] == dados['codigo'] for e in empresas):
            return jsonify({'error': 'Código já existe'}), 400
        
        # Criar nova empresa
        nova_empresa = {
            'codigo': dados['codigo'],
            'nome': dados['nome'],
            'url': dados.get('url', ''),
            'ativo': dados.get('ativo', True),
            'observacoes': dados.get('observacoes', '')
        }
        
        empresas.append(nova_empresa)
        
        if salvar_empresas(empresas):
            log_sistema(f"Nova empresa criada: {nova_empresa['codigo']} - {nova_empresa['nome']}", "success")
            return jsonify(nova_empresa), 201
        else:
            return jsonify({'error': 'Erro ao salvar empresa'}), 500
            
    except Exception as e:
        log_sistema(f"Erro ao criar empresa: {str(e)}", "error")
        return jsonify({'error': str(e)}), 500

@app.route('/api/empresas/<codigo>', methods=['PUT'])
def api_editar_empresa(codigo):
    """API para editar empresa"""
    try:
        dados = request.get_json()
        empresas = carregar_empresas()
        
        # Encontrar empresa
        empresa_idx = None
        for i, empresa in enumerate(empresas):
            if empresa['codigo'] == codigo:
                empresa_idx = i
                break
        
        if empresa_idx is None:
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        # Atualizar dados
        empresas[empresa_idx].update({
            'nome': dados.get('nome', empresas[empresa_idx]['nome']),
            'url': dados.get('url', empresas[empresa_idx].get('url', '')),
            'ativo': dados.get('ativo', empresas[empresa_idx].get('ativo', True)),
            'observacoes': dados.get('observacoes', empresas[empresa_idx].get('observacoes', ''))
        })
        
        if salvar_empresas(empresas):
            log_sistema(f"Empresa editada: {codigo}", "success")
            return jsonify(empresas[empresa_idx])
        else:
            return jsonify({'error': 'Erro ao salvar alterações'}), 500
            
    except Exception as e:
        log_sistema(f"Erro ao editar empresa: {str(e)}", "error")
        return jsonify({'error': str(e)}), 500

@app.route('/api/empresas/<codigo>', methods=['DELETE'])
def api_excluir_empresa(codigo):
    """API para excluir empresa"""
    try:
        empresas = carregar_empresas()
        
        # Filtrar empresa
        empresas_filtradas = [e for e in empresas if e['codigo'] != codigo]
        
        if len(empresas_filtradas) == len(empresas):
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        if salvar_empresas(empresas_filtradas):
            log_sistema(f"Empresa excluída: {codigo}", "success")
            return jsonify({'message': 'Empresa excluída com sucesso'})
        else:
            return jsonify({'error': 'Erro ao excluir empresa'}), 500
            
    except Exception as e:
        log_sistema(f"Erro ao excluir empresa: {str(e)}", "error")
        return jsonify({'error': str(e)}), 500

# APIs REST para grupos
@app.route('/api/grupos', methods=['GET'])
def api_listar_grupos():
    """API para listar grupos"""
    grupos = carregar_grupos()
    return jsonify(grupos)

@app.route('/api/grupos', methods=['POST'])
def api_criar_grupo():
    """API para criar novo grupo"""
    try:
        dados = request.get_json()
        grupos = carregar_grupos()
        
        # Validar dados obrigatórios
        if not dados.get('nome'):
            return jsonify({'error': 'Nome é obrigatório'}), 400
        
        # Criar novo grupo
        novo_grupo = {
            'nome': dados['nome'],
            'descricao': dados.get('descricao', ''),
            'ativo': dados.get('ativo', True)
        }
        
        grupos.append(novo_grupo)
        
        if salvar_grupos(grupos):
            log_sistema(f"Novo grupo criado: {novo_grupo['nome']}", "success")
            return jsonify(novo_grupo), 201
        else:
            return jsonify({'error': 'Erro ao salvar grupo'}), 500
            
    except Exception as e:
        log_sistema(f"Erro ao criar grupo: {str(e)}", "error")
        return jsonify({'error': str(e)}), 500

@app.route('/api/grupos/<int:index>', methods=['PUT'])
def api_editar_grupo(index):
    """API para editar grupo"""
    try:
        dados = request.get_json()
        grupos = carregar_grupos()
        
        if index < 0 or index >= len(grupos):
            return jsonify({'error': 'Grupo não encontrado'}), 404
        
        # Atualizar dados
        grupos[index].update({
            'nome': dados.get('nome', grupos[index]['nome']),
            'descricao': dados.get('descricao', grupos[index].get('descricao', '')),
            'ativo': dados.get('ativo', grupos[index].get('ativo', True))
        })
        
        if salvar_grupos(grupos):
            log_sistema(f"Grupo editado: {grupos[index]['nome']}", "success")
            return jsonify(grupos[index])
        else:
            return jsonify({'error': 'Erro ao salvar alterações'}), 500
            
    except Exception as e:
        log_sistema(f"Erro ao editar grupo: {str(e)}", "error")
        return jsonify({'error': str(e)}), 500

@app.route('/api/grupos/<int:index>', methods=['DELETE'])
def api_excluir_grupo(index):
    """API para excluir grupo"""
    try:
        grupos = carregar_grupos()
        
        if index < 0 or index >= len(grupos):
            return jsonify({'error': 'Grupo não encontrado'}), 404
        
        grupo_nome = grupos[index]['nome']
        grupos.pop(index)
        
        if salvar_grupos(grupos):
            log_sistema(f"Grupo excluído: {grupo_nome}", "success")
            return jsonify({'message': 'Grupo excluído com sucesso'})
        else:
            return jsonify({'error': 'Erro ao excluir grupo'}), 500
            
    except Exception as e:
        log_sistema(f"Erro ao excluir grupo: {str(e)}", "error")
        return jsonify({'error': str(e)}), 500

# APIs de operações (modo demo)
@app.route('/api/gerar-prints', methods=['POST'])
def api_gerar_prints():
    """API para gerar prints (modo demo)"""
    global operacao_em_andamento
    
    if operacao_em_andamento:
        return jsonify({'error': 'Operação já em andamento'}), 400
    
    def simular_geracao():
        global operacao_em_andamento
        operacao_em_andamento = True
        
        try:
            empresas = carregar_empresas()
            empresas_ativas = [e for e in empresas if e.get('ativo', True)]
            
            log_sistema("🖼️ Iniciando geração de prints...", "info")
            
            for i, empresa in enumerate(empresas_ativas):
                log_sistema(f"📸 Gerando print para {empresa['nome']}...", "info")
                time.sleep(2)  # Simular processamento
                log_sistema(f"✅ Print gerado para {empresa['nome']}", "success")
                
                # Emitir progresso
                progresso = int((i + 1) / len(empresas_ativas) * 100)
                socketio.emit('operacao_progresso', {
                    'operacao': 'gerar_prints',
                    'progresso': progresso,
                    'empresa_atual': empresa['nome']
                })
            
            log_sistema("🎉 Geração de prints concluída!", "success")
            
        except Exception as e:
            log_sistema(f"❌ Erro na geração de prints: {str(e)}", "error")
        finally:
            operacao_em_andamento = False
            socketio.emit('operacao_concluida', {'operacao': 'gerar_prints'})
    
    # Executar em thread separada
    thread = threading.Thread(target=simular_geracao)
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'Geração de prints iniciada'})

@app.route('/api/enviar-whatsapp', methods=['POST'])
def api_enviar_whatsapp():
    """API para enviar WhatsApp (modo demo)"""
    global operacao_em_andamento
    
    if operacao_em_andamento:
        return jsonify({'error': 'Operação já em andamento'}), 400
    
    def simular_envio():
        global operacao_em_andamento
        operacao_em_andamento = True
        
        try:
            grupos = carregar_grupos()
            grupos_ativos = [g for g in grupos if g.get('ativo', True)]
            
            log_sistema("📱 Iniciando envio para WhatsApp...", "info")
            
            for i, grupo in enumerate(grupos_ativos):
                log_sistema(f"📤 Enviando para {grupo['nome']}...", "info")
                time.sleep(3)  # Simular envio
                log_sistema(f"✅ Enviado para {grupo['nome']}", "success")
                
                # Emitir progresso
                progresso = int((i + 1) / len(grupos_ativos) * 100)
                socketio.emit('operacao_progresso', {
                    'operacao': 'enviar_whatsapp',
                    'progresso': progresso,
                    'grupo_atual': grupo['nome']
                })
            
            log_sistema("🎉 Envio para WhatsApp concluído!", "success")
            
        except Exception as e:
            log_sistema(f"❌ Erro no envio WhatsApp: {str(e)}", "error")
        finally:
            operacao_em_andamento = False
            socketio.emit('operacao_concluida', {'operacao': 'enviar_whatsapp'})
    
    # Executar em thread separada
    thread = threading.Thread(target=simular_envio)
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'Envio para WhatsApp iniciado'})

@app.route('/api/processo-completo', methods=['POST'])
def api_processo_completo():
    """API para processo completo (modo demo)"""
    global operacao_em_andamento
    
    if operacao_em_andamento:
        return jsonify({'error': 'Operação já em andamento'}), 400
    
    def simular_processo_completo():
        global operacao_em_andamento
        operacao_em_andamento = True
        
        try:
            empresas = carregar_empresas()
            grupos = carregar_grupos()
            empresas_ativas = [e for e in empresas if e.get('ativo', True)]
            grupos_ativos = [g for g in grupos if g.get('ativo', True)]
            
            total_etapas = len(empresas_ativas) + len(grupos_ativos)
            etapa_atual = 0
            
            log_sistema("🚀 Iniciando processo completo...", "info")
            
            # Fase 1: Gerar prints
            log_sistema("📸 Fase 1: Gerando prints...", "info")
            for empresa in empresas_ativas:
                log_sistema(f"📸 Gerando print para {empresa['nome']}...", "info")
                time.sleep(2)
                etapa_atual += 1
                progresso = int(etapa_atual / total_etapas * 100)
                socketio.emit('operacao_progresso', {
                    'operacao': 'processo_completo',
                    'progresso': progresso,
                    'fase': 'Gerando prints',
                    'item_atual': empresa['nome']
                })
            
            log_sistema("✅ Prints gerados com sucesso!", "success")
            
            # Fase 2: Enviar WhatsApp
            log_sistema("📱 Fase 2: Enviando para WhatsApp...", "info")
            for grupo in grupos_ativos:
                log_sistema(f"📤 Enviando para {grupo['nome']}...", "info")
                time.sleep(3)
                etapa_atual += 1
                progresso = int(etapa_atual / total_etapas * 100)
                socketio.emit('operacao_progresso', {
                    'operacao': 'processo_completo',
                    'progresso': progresso,
                    'fase': 'Enviando WhatsApp',
                    'item_atual': grupo['nome']
                })
            
            log_sistema("🎉 Processo completo finalizado!", "success")
            
        except Exception as e:
            log_sistema(f"❌ Erro no processo completo: {str(e)}", "error")
        finally:
            operacao_em_andamento = False
            socketio.emit('operacao_concluida', {'operacao': 'processo_completo'})
    
    # Executar em thread separada
    thread = threading.Thread(target=simular_processo_completo)
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'Processo completo iniciado'})

@app.route('/api/stats')
def api_stats():
    """API para obter estatísticas"""
    return jsonify(obter_estatisticas())

@app.route('/health')
def health():
    """Rota de healthcheck para o Railway"""
    return {'status': 'ok', 'message': 'UPAUDIT funcionando!'}, 200

@app.route('/ping')
def ping():
    """Rota alternativa de healthcheck"""
    return 'pong', 200

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Cliente conectado"""
    log_sistema("Cliente conectado ao WebSocket", "info")
    emit('connected', {'data': 'Conectado ao sistema'})

@socketio.on('disconnect')
def handle_disconnect():
    """Cliente desconectado"""
    print("Cliente desconectado")

# Inicialização
if __name__ == '__main__':
    print("🔧 Sistema inicializado")
    log_sistema("Sistema inicializado com sucesso")
    
    print("🚀 Iniciando Sistema de Auditoria Web")
    print("📊 Dashboard disponível em: http://localhost:5000")
    print("🔧 Modo de desenvolvimento ativo")
    
    # Executar aplicação
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True) 