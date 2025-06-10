@echo off
chcp 65001 >nul
title 🚀 UPAUDIT - Upload para GitHub

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🚀 UPAUDIT - UPLOAD PARA GITHUB               ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🔧 Preparando upload para GitHub...
echo.

REM Verificar se Git está instalado
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git não está instalado!
    echo 📥 Baixe em: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo ✅ Git encontrado!
echo.

REM Inicializar repositório se não existir
if not exist ".git" (
    echo 🔧 Inicializando repositório Git...
    git init
    echo.
)

REM Configurar Git se necessário
echo 🔧 Configurando Git...
set /p GIT_NAME="Digite seu nome para o Git (ex: João Silva): "
set /p GIT_EMAIL="Digite seu email do GitHub (ex: joao@email.com): "

git config user.name "%GIT_NAME%"
git config user.email "%GIT_EMAIL%"
echo.

REM Adicionar todos os arquivos
echo 📁 Adicionando arquivos ao Git...
git add .
echo.

REM Fazer commit
echo 💾 Fazendo commit...
set COMMIT_MSG=🚀 UPAUDIT - Sistema de Auditoria Web Completo
git commit -m "%COMMIT_MSG%"
echo.

REM Solicitar URL do repositório
echo 🌐 Agora você precisa criar um repositório no GitHub:
echo    1. Acesse: https://github.com/new
echo    2. Nome sugerido: upaudit-sistema
echo    3. Deixe como público
echo    4. NÃO marque "Add a README file"
echo    5. Clique em "Create repository"
echo.
pause

set /p REPO_URL="Cole a URL do repositório (ex: https://github.com/seuusuario/upaudit-sistema.git): "

REM Adicionar origin
echo 🔗 Conectando ao repositório remoto...
git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%
echo.

REM Fazer push
echo 🚀 Enviando para GitHub...
git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ✅ SUCESSO! Projeto enviado para GitHub!
    echo 🌐 Seu repositório: %REPO_URL%
    echo.
    echo 🎯 PRÓXIMOS PASSOS:
    echo    1. Acesse seu repositório no GitHub
    echo    2. Execute: DEPLOY_RAPIDO.bat
    echo    3. Siga o guia de deploy
    echo.
) else (
    echo.
    echo ❌ ERRO no upload!
    echo 💡 Possíveis soluções:
    echo    - Verifique se a URL está correta
    echo    - Faça login no Git: git config --global credential.helper manager
    echo    - Tente novamente
    echo.
)

pause 