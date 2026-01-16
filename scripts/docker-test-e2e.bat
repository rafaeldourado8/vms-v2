@echo off
echo ========================================
echo GT-Vision VMS - Build e Teste E2E
echo ========================================
echo.

echo [1/3] Fazendo build das imagens...
docker-compose -f docker-compose.dev.yml build streaming detection
if errorlevel 1 (
    echo ERRO: Build falhou
    pause
    exit /b 1
)
echo.

echo [2/3] Iniciando todos os servicos...
docker-compose -f docker-compose.dev.yml up -d
if errorlevel 1 (
    echo ERRO: Falha ao iniciar servicos
    pause
    exit /b 1
)
echo.

echo [3/3] Aguardando servicos iniciarem...
timeout /t 15 >nul
echo.

echo ========================================
echo Servicos rodando!
echo ========================================
echo.
echo URLs:
echo   Streaming API:  http://localhost:8001/docs
echo   Detection API:  http://localhost:8002/docs
echo   MediaMTX HLS:   http://localhost:8889
echo   Grafana:        http://localhost:3000
echo   Kibana:         http://localhost:5601
echo   RabbitMQ:       http://localhost:15672
echo   MinIO:          http://localhost:9001
echo.
echo Executando teste E2E...
echo.
python scripts\test_docker_e2e.py
echo.
echo ========================================
echo Para ver logs: docker-compose -f docker-compose.dev.yml logs -f
echo Para parar:    docker-compose -f docker-compose.dev.yml down
echo ========================================
pause
