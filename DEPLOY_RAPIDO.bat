@echo off
chcp 65001 >nul
title 🚀 UPAUDIT - Deploy Rápido

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🚀 UPAUDIT - DEPLOY RÁPIDO                ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🔧 Preparando sistema para deploy...
echo.

echo 📋 1. Verificando arquivos necessários...
if exist "requirements.txt" (
    echo ✅ requirements.txt - OK
) else (
    echo ❌ requirements.txt - FALTANDO
    pause
    exit
)

if exist "Procfile" (
    echo ✅ Procfile - OK
) else (
    echo ❌ Procfile - FALTANDO
    pause
    exit
)

if exist "app.py" (
    echo ✅ app.py - OK
) else (
    echo ❌ app.py - FALTANDO
    pause
    exit
)

echo.
echo 🔐 2. Chave secreta necessária...
echo    Use este comando para gerar: python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"

echo.
echo 📚 3. Abrindo guia de deploy...
start DEPLOY_GUIDE.md

echo.
echo ✅ SISTEMA PRONTO PARA DEPLOY!
echo.
echo 🎯 PRÓXIMOS PASSOS:
echo    1. Escolha uma plataforma (Railway recomendado)
echo    2. Siga o guia que foi aberto
echo    3. Configure as variáveis de ambiente
echo    4. Faça o deploy!
echo.
echo 🌐 PLATAFORMAS DISPONÍVEIS:
echo    • Railway: https://railway.app
echo    • Render: https://render.com  
echo    • PythonAnywhere: https://pythonanywhere.com
echo    • Heroku: https://heroku.com
echo.

pause 