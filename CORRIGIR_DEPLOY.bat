@echo off
chcp 65001 >nul
title 🔧 UPAUDIT - Corrigir Deploy

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🔧 UPAUDIT - CORRIGIR DEPLOY                  ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🔧 Corrigindo problemas de deploy...
echo.

echo ✅ 1. Requirements.txt otimizado
echo ✅ 2. Nixpacks.toml criado (Railway)
echo ✅ 3. Configurações de produção adicionadas
echo.

echo 📋 SOLUÇÕES APLICADAS:
echo    • Removidas dependências desnecessárias
echo    • Adicionado suporte ao Chrome/Chromium
echo    • Configurações específicas para Railway
echo    • Otimizações para Selenium em produção
echo.

echo 🚀 FAZER NOVO DEPLOY:
echo.
echo 1. Commit as correções:
git add .
git commit -m "🔧 Correções para deploy em produção"
git push

echo.
echo 2. No Railway:
echo    • Vá em "Deployments"
echo    • Clique em "Redeploy"
echo    • Aguarde o build
echo.

echo 3. Variáveis de ambiente necessárias:
echo    FLASK_ENV=production
echo    FLASK_DEBUG=False
echo    SECRET_KEY=9225e5fe046b4e9eb11f276f751c9ed8072a34f0371f3deff0137ff6f4889174
echo    SELENIUM_HEADLESS=True
echo    CHROME_BIN=/usr/bin/chromium
echo    CHROMEDRIVER_PATH=/usr/bin/chromedriver
echo.

echo ✅ CORREÇÕES APLICADAS! Faça o redeploy no Railway.
echo.

pause 