# 🚀 Guia de Deploy - UPAUDIT

## 🌐 Hospedagem Gratuita com Domínio

Este guia mostra como colocar o UPAUDIT online gratuitamente com domínio próprio.

---

## 🎯 **Opção 1: Railway (RECOMENDADO)**

### ✅ **Vantagens**
- ✅ Deploy super fácil
- ✅ Domínio gratuito: `upaudit.up.railway.app`
- ✅ SSL automático
- ✅ 500 horas/mês grátis
- ✅ Suporte completo ao Flask

### 📋 **Passo a Passo**

#### **1. Preparar o Código**
```bash
# Já está pronto! Os arquivos necessários foram criados:
# - Procfile
# - requirements.txt
# - runtime.txt
# - railway.json
```

#### **2. Criar Conta no Railway**
1. Acesse: https://railway.app
2. Clique em "Start a New Project"
3. Faça login com GitHub

#### **3. Fazer Deploy**
1. **Opção A - Via GitHub (Recomendado):**
   - Suba o código para um repositório GitHub
   - No Railway: "Deploy from GitHub repo"
   - Selecione seu repositório
   - Deploy automático!

2. **Opção B - Via CLI:**
   ```bash
   npm install -g @railway/cli
   railway login
   railway init
   railway up
   ```

#### **4. Configurar Variáveis de Ambiente**
No painel do Railway, adicione:
```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=9225e5fe046b4e9eb11f276f751c9ed8072a34f0371f3deff0137ff6f4889174
SELENIUM_HEADLESS=True
```

#### **5. Acessar o Sistema**
- URL: `https://upaudit-production.up.railway.app`
- Funcionando 24/7!

---

## 🎯 **Opção 2: Render**

### ✅ **Vantagens**
- ✅ 750 horas/mês grátis
- ✅ Domínio: `upaudit.onrender.com`
- ✅ Deploy via GitHub
- ✅ SSL gratuito

### 📋 **Passo a Passo**

#### **1. Criar Conta**
1. Acesse: https://render.com
2. Faça login com GitHub

#### **2. Criar Web Service**
1. "New" → "Web Service"
2. Conecte seu repositório GitHub
3. Configurações:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT app:app`
   - **Python Version**: 3.11.6

#### **3. Variáveis de Ambiente**
```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=sua_chave_secreta
SELENIUM_HEADLESS=True
```

---

## 🎯 **Opção 3: PythonAnywhere**

### ✅ **Vantagens**
- ✅ Especializado em Python
- ✅ Domínio: `seuusuario.pythonanywhere.com`
- ✅ Interface web amigável

### 📋 **Passo a Passo**

#### **1. Criar Conta**
1. Acesse: https://www.pythonanywhere.com
2. Crie conta gratuita

#### **2. Upload dos Arquivos**
1. Vá em "Files"
2. Faça upload de todos os arquivos do projeto
3. Ou clone via Git:
   ```bash
   git clone https://github.com/seuusuario/upaudit.git
   ```

#### **3. Criar Web App**
1. "Web" → "Add a new web app"
2. Escolha "Flask"
3. Python 3.10
4. Configure o arquivo WSGI

#### **4. Configurar WSGI**
Edite `/var/www/seuusuario_pythonanywhere_com_wsgi.py`:
```python
import sys
import os

# Adiciona o diretório do projeto
project_home = '/home/seuusuario/upaudit'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Importa a aplicação
from app import app as application

if __name__ == "__main__":
    application.run()
```

---

## 🎯 **Opção 4: Heroku**

### ⚠️ **Limitações**
- ⚠️ Apenas 550 horas/mês
- ⚠️ Dorme após 30min de inatividade

### 📋 **Passo a Passo**

#### **1. Instalar Heroku CLI**
```bash
# Windows
winget install Heroku.CLI

# Ou baixe de: https://devcenter.heroku.com/articles/heroku-cli
```

#### **2. Deploy**
```bash
heroku login
heroku create upaudit-sistema
git add .
git commit -m "Deploy UPAUDIT"
git push heroku main
```

---

## 🔧 **Configurações Importantes**

### 🛡️ **Segurança**
```bash
# Gere uma chave secreta forte:
python -c "import secrets; print(secrets.token_hex(32))"
```

### 🐛 **Debug em Produção**
- Sempre use `FLASK_DEBUG=False`
- Configure logs adequados
- Use `SELENIUM_HEADLESS=True`

### 📊 **Monitoramento**
- Railway: Painel com logs em tempo real
- Render: Logs e métricas
- PythonAnywhere: Logs de erro
- Heroku: `heroku logs --tail`

---

## 🎉 **Domínio Personalizado (Opcional)**

### 🆓 **Domínios Gratuitos**
1. **Freenom**: `.tk`, `.ml`, `.ga`, `.cf`
2. **Dot.tk**: Domínios `.tk` gratuitos
3. **No-IP**: Subdomínios gratuitos

### 🔗 **Configurar DNS**
1. Registre domínio gratuito
2. Configure CNAME:
   ```
   CNAME: upaudit.seudominio.tk → upaudit.up.railway.app
   ```

---

## 🚀 **Recomendação Final**

### 🥇 **Para Iniciantes: Railway**
- Mais fácil de usar
- Deploy automático
- Boa documentação

### 🥈 **Para Desenvolvedores: Render**
- Mais recursos
- Melhor para projetos maiores
- Deploy via GitHub

### 🥉 **Para Python: PythonAnywhere**
- Interface amigável
- Suporte especializado
- Boa para aprender

---

## 📞 **Suporte**

### 🆘 **Problemas Comuns**

1. **Erro de Build**:
   - Verifique `requirements.txt`
   - Confirme versão do Python

2. **App não inicia**:
   - Verifique variáveis de ambiente
   - Confira logs da plataforma

3. **Selenium não funciona**:
   - Use `SELENIUM_HEADLESS=True`
   - Instale dependências do Chrome

### 📚 **Documentação**
- [Railway Docs](https://docs.railway.app)
- [Render Docs](https://render.com/docs)
- [PythonAnywhere Help](https://help.pythonanywhere.com)
- [Heroku Docs](https://devcenter.heroku.com)

---

**🎯 Escolha a plataforma que mais se adequa ao seu perfil e coloque o UPAUDIT online em minutos!** 