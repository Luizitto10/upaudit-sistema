@echo off
title Sistema de Auditoria Web
color 0A

echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║                    SISTEMA DE AUDITORIA WEB                  ║
echo  ║                                                              ║
echo  ║  🚀 Transformando seu sistema desktop em aplicacao web!     ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.
echo  📊 Dashboard: http://localhost:5000
echo  🌐 Acesso local: http://127.0.0.1:5000
echo  🔗 Acesso rede: http://192.168.0.10:5000
echo.
echo  ⚡ Iniciando servidor...
echo.

python app.py

echo.
echo  ❌ Servidor parado. Pressione qualquer tecla para sair...
pause >nul 