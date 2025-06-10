# 🌐 Sistema de Auditoria Web

## 🎯 Visão Geral
Sistema web moderno para geração automática de prints de auditoria e envio via WhatsApp. Transformação completa do sistema desktop em aplicação web responsiva.

## ✨ Funcionalidades Principais

### 📊 **Dashboard Interativo**
- Estatísticas em tempo real
- Controles rápidos de execução
- Logs em tempo real via WebSocket
- Progresso visual das operações

### 🚀 **Operações Automatizadas**
- **Geração de Prints**: Screenshots automáticos dos relatórios
- **Envio WhatsApp**: Envio automático para grupos
- **Processo Completo**: Execução sequencial (prints + envio)
- **Modo Invisível**: Execução em background

### 📝 **CRUD Completo**
- **Empresas**: Criar, editar, excluir e gerenciar empresas
- **Grupos WhatsApp**: Gerenciar grupos e associações
- **Validações**: Códigos únicos e campos obrigatórios
- **Persistência**: Salvamento automático em arquivos JSON

### 📱 **Interface Moderna**
- Design responsivo (desktop/mobile)
- Atualizações em tempo real
- Interface intuitiva e profissional
- Controles visuais de progresso

## 🚀 Como Usar

### 1️⃣ **Uso Local**
```bash
# Clique duas vezes no arquivo:
INICIAR_SISTEMA_WEB.bat
```

### 2️⃣ **Deploy Online (NOVO!) 🌐**
```bash
# Para colocar online com domínio gratuito:
DEPLOY_RAPIDO.bat
```
📖 **Guia Completo**: [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)

### 3️⃣ **Acessar o Dashboard**
- **Local**: http://localhost:5000
- **Online**: Seu domínio após deploy
- O dashboard será carregado automaticamente

### 3️⃣ **Executar Operações**
1. **Processo Completo** (Recomendado):
   - Clique em "Executar Completo" no dashboard
   - Acompanhe o progresso em tempo real

2. **Operações Individuais**:
   - Vá para "Operações" no menu
   - Escolha "Gerar Prints" ou "Enviar WhatsApp"
   - Configure modo invisível se necessário

## 📁 Estrutura do Sistema

```
📁 PROJETO AUDIT - WEB/
├── 🐍 app.py                    # Servidor Flask principal
├── 🔧 central_audit.py          # Lógica de automação
├── ⚙️ config_manager.py         # Gerenciador de configurações
├── 📊 empresas.json             # Dados das empresas
├── 📱 grupos_whatsapp.json      # Grupos do WhatsApp
├── ⚙️ config.json               # Configurações do sistema
├── 📁 templates/                # Páginas HTML
│   ├── base.html               # Template base
│   ├── dashboard.html          # Dashboard principal
│   ├── operacoes.html          # Página de operações
│   ├── empresas.html           # Gerenciamento de empresas
│   └── grupos.html             # Grupos WhatsApp
├── 📁 static/                   # Recursos web (CSS, JS, imagens)
├── 📁 prints/                   # Screenshots gerados
├── 📁 logs/                     # Logs do sistema
└── 🚀 INICIAR_SISTEMA_WEB.bat   # Inicializador
```

## 🔧 Configurações

### **Empresas** (`empresas.json`)
```json
{
    "codigo": 27119,
    "nome": "Matercaldas",
    "grupo": "UP + MATERCALDAS",
    "nome_arquivo": "27119 - Matercaldas.png",
    "ativo": true
}
```

### **Grupos WhatsApp** (`grupos_whatsapp.json`)
```json
{
    "grupo": "UPAUDIT + EQUILIBRIO",
    "arquivo": "16289 - Equilibrio Homeopatia.png",
    "empresa": "Equilibrio Homeopatia",
    "ativo": true
}
```

## 📊 Páginas do Sistema

### 🏠 **Dashboard** (`/`)
- Estatísticas principais
- Controles rápidos
- Logs em tempo real
- Status do sistema

### ⚡ **Operações** (`/operacoes`)
- Controles detalhados
- Configurações de modo
- Progresso detalhado
- Logs específicos

### 🏢 **Empresas** (`/empresas`)
- Lista de empresas com CRUD completo
- Criar, editar e excluir empresas
- Status ativo/inativo
- Validação de códigos únicos

### 📱 **Grupos WhatsApp** (`/grupos`)
- Lista de grupos com CRUD completo
- Criar, editar e excluir grupos
- Empresas por grupo
- Status ativo/inativo
- Resumo visual por grupo

### ⚙️ **Configurações** (`/configuracoes`)
- Configurações do sistema
- Parâmetros de automação

## 🔄 Atualizações em Tempo Real

O sistema utiliza **WebSocket** para:
- ✅ Progresso das operações
- 📝 Logs em tempo real
- 📊 Atualizações de status
- 🔔 Notificações de conclusão

## 🛠️ Tecnologias Utilizadas

- **Backend**: Flask + Flask-SocketIO
- **Frontend**: Bootstrap 5 + JavaScript
- **Automação**: Selenium WebDriver
- **Dados**: JSON (empresas e grupos)
- **Logs**: Sistema integrado

## 📋 Manual do CRUD

Para instruções detalhadas sobre como usar as funcionalidades de CRUD (Criar, Ler, Atualizar, Deletar), consulte:

**📖 [CRUD_MANUAL.md](CRUD_MANUAL.md)**

Este manual contém:
- ➕ Como adicionar empresas e grupos
- ✏️ Como editar registros existentes
- 🗑️ Como excluir registros
- 🔧 Solução de problemas
- 💡 Dicas importantes

## 📞 Suporte

### **Problemas Comuns**

1. **Erro ao carregar grupos**:
   - Verifique se `grupos_whatsapp.json` existe
   - Confirme formato JSON válido

2. **WhatsApp não conecta**:
   - Faça login no WhatsApp Web manualmente
   - Verifique se Chrome está atualizado

3. **Prints não são gerados**:
   - Confirme credenciais em `config.json`
   - Verifique conexão com sistema de auditoria

### **Logs do Sistema**
- Logs em tempo real no dashboard
- Arquivos de log em `logs/`
- Debug via console do navegador

## 🎉 Vantagens do Sistema Web

✅ **Acesso Remoto**: Use de qualquer dispositivo
✅ **Interface Moderna**: Design profissional e responsivo
✅ **Tempo Real**: Acompanhe operações instantaneamente
✅ **Multi-usuário**: Vários usuários podem acessar
✅ **Sem Instalação**: Funciona direto no navegador
✅ **Logs Centralizados**: Histórico completo de operações

## 🌐 Hospedagem Online

### 🆓 **Opções Gratuitas com Domínio**

| Plataforma | Domínio | Limite | Facilidade |
|------------|---------|--------|------------|
| 🚀 **Railway** | `upaudit.up.railway.app` | 500h/mês | ⭐⭐⭐⭐⭐ |
| ⚡ **Render** | `upaudit.onrender.com` | 750h/mês | ⭐⭐⭐⭐ |
| 🐍 **PythonAnywhere** | `usuario.pythonanywhere.com` | 1 app | ⭐⭐⭐ |
| 🔥 **Heroku** | `upaudit.herokuapp.com` | 550h/mês | ⭐⭐ |

### 🎯 **Recomendação**
- **Iniciantes**: Railway (mais fácil)
- **Desenvolvedores**: Render (mais recursos)
- **Python**: PythonAnywhere (especializado)

### 📚 **Documentação Completa**
📖 **[DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)** - Guia passo a passo para todas as plataformas

---

**🚀 Sistema desenvolvido para máxima eficiência e facilidade de uso!** 