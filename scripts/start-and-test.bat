@echo off
echo ========================================
echo GT-Vision VMS - Iniciar e Testar
echo ========================================
echo.

echo [1/4] Iniciando servicos essenciais...
docker-compose -f docker-compose.dev.yml up -d postgres redis rabbitmq minio mediamtx
echo.

echo Aguardando servicos (30s)...
timeout /t 30 /nobreak
echo.

echo [2/4] Verificando servicos...
docker-compose -f docker-compose.dev.yml ps
echo.

echo [3/4] Testando conectividade...
echo.
echo PostgreSQL (5432):
netstat -an | findstr "5432" | findstr "LISTENING"
echo.
echo Redis (6379):
netstat -an | findstr "6379" | findstr "LISTENING"
echo.
echo RabbitMQ (5672, 15672):
netstat -an | findstr "5672" | findstr "LISTENING"
netstat -an | findstr "15672" | findstr "LISTENING"
echo.
echo MinIO (9000):
netstat -an | findstr "9000" | findstr "LISTENING"
echo.
echo MediaMTX (8554, 8888):
netstat -an | findstr "8554" | findstr "LISTENING"
netstat -an | findstr "8888" | findstr "LISTENING"
echo.

echo [4/4] Executando smoke test...
poetry run python tests/smoke_test.py
echo.

echo ========================================
echo Pronto para desenvolvimento!
echo ========================================
echo.
echo Proximos passos:
echo   1. Iniciar Django:  poetry run python manage.py runserver
echo   2. Iniciar FastAPI: cd src/streaming ^&^& poetry run uvicorn infrastructure.web.main:app --reload --port 8001
echo   3. Executar testes: scripts\test-sprint13.bat
echo.
