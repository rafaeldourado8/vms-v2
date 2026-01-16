@echo off
REM GT-Vision VMS - Start Full Stack (Docker)
REM Inicia toda a stack no Docker (infraestrutura + aplicações)

echo ========================================
echo GT-Vision VMS - Full Stack Docker
echo ========================================
echo.

echo [1/4] Parando containers antigos...
docker-compose down

echo.
echo [2/4] Construindo imagens...
docker-compose build

echo.
echo [3/4] Iniciando stack completa...
docker-compose up -d

echo.
echo [4/4] Aguardando serviços iniciarem (30s)...
timeout /t 30 /nobreak

echo.
echo ========================================
echo Stack iniciada com sucesso!
echo ========================================
echo.
echo Serviços disponíveis:
echo.
echo APLICAÇÕES:
echo   - Django Admin:      http://localhost:8000/admin
echo   - Streaming API:     http://localhost:8001/docs
echo.
echo INFRAESTRUTURA:
echo   - PostgreSQL:        localhost:5432
echo   - Redis:             localhost:6379
echo   - RabbitMQ:          http://localhost:15672 (gtvision/gtvision_password)
echo   - MinIO:             http://localhost:9001 (minioadmin/minioadmin)
echo   - MediaMTX:          rtsp://localhost:8554
echo.
echo OBSERVABILIDADE:
echo   - Prometheus:        http://localhost:9090
echo   - Grafana:           http://localhost:3000 (admin/admin)
echo   - Kibana:            http://localhost:5601
echo.
echo COMANDOS ÚTEIS:
echo   - Ver logs:          docker-compose logs -f
echo   - Parar stack:       docker-compose down
echo   - Reiniciar:         docker-compose restart
echo.
echo ========================================

pause
