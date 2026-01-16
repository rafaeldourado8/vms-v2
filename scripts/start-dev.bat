@echo off
REM GT-Vision VMS - Start Development Environment
REM Infraestrutura no Docker + Backend/Streaming localmente

echo ========================================
echo GT-Vision VMS - Development Environment
echo ========================================
echo.

echo [1/5] Parando containers antigos...
docker-compose -f docker-compose.dev.yml down

echo.
echo [2/5] Iniciando infraestrutura (Docker)...
docker-compose -f docker-compose.dev.yml up -d

echo.
echo [3/5] Aguardando serviços iniciarem (30s)...
timeout /t 30 /nobreak

echo.
echo [4/5] Inicializando buckets MinIO...
poetry run python scripts\init_minio.py

echo.
echo [5/5] Aplicando migrations...
poetry run python manage.py migrate

echo.
echo ========================================
echo Infraestrutura iniciada com sucesso!
echo ========================================
echo.
echo INFRAESTRUTURA (Docker):
echo   - PostgreSQL:        localhost:5432
echo   - Redis:             localhost:6379
echo   - RabbitMQ:          http://localhost:15672 (gtvision/gtvision_password)
echo   - MinIO:             http://localhost:9001 (minioadmin/minioadmin)
echo   - MediaMTX RTSP:     rtsp://localhost:8554
echo   - MediaMTX HLS:      http://localhost:8888
echo.
echo OBSERVABILIDADE (Docker):
echo   - Prometheus:        http://localhost:9090
echo   - Grafana:           http://localhost:3000 (admin/admin)
echo   - Elasticsearch:     http://localhost:9200
echo   - Logstash:          localhost:5000
echo   - Kibana:            http://localhost:5601
echo.
echo ========================================
echo PROXIMO PASSO: Iniciar aplicacoes localmente
echo ========================================
echo.
echo Terminal 1 - Django (Admin + Cidades):
echo   poetry run python manage.py runserver
echo.
echo Terminal 2 - FastAPI (Streaming + AI):
echo   cd src/streaming
echo   poetry run uvicorn infrastructure.web.main:app --reload --port 8001
echo.
echo ========================================

pause
