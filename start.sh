#!/bin/bash
echo "🚀 Iniciando UPAUDIT no Railway..."
echo "📊 Porta: $PORT"
echo "🔧 Executando gunicorn..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --access-logfile - --error-logfile - app:app 