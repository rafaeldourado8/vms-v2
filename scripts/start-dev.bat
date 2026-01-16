@echo off
echo ========================================
echo GT-Vision VMS - Ambiente Dev
echo Apenas Infraestrutura
echo ========================================
echo.

echo [1/2] Iniciando infraestrutura...
docker-compose -f docker-compose.dev.yml up -d
echo.

echo Aguardando servicos (30s)...
timeout /t 30 /nobreak
echo.

echo [2/2] Status dos servicos...
docker-compose -f docker-compose.dev.yml ps
echo.

echo ========================================
echo Infraestrutura Pronta!
echo ========================================
echo.
echo Servicos disponiveis:
echo   PostgreSQL:    localhost:5432
echo   Redis:         localhost:6379
echo   RabbitMQ:      localhost:5672, 15672
echo   MinIO:         localhost:9000, 9001
echo   MediaMTX:      localhost:8554, 8888, 8889
echo   Prometheus:    localhost:9090
echo   Grafana:       localhost:3000
echo   Elasticsearch: localhost:9200
echo   Kibana:        localhost:5601
echo.
echo Proximos passos:
echo   1. Rodar Django:  poetry run python manage.py runserver
echo   2. Rodar FastAPI: cd src/streaming ^&^& poetry run uvicorn infrastructure.web.main:app --reload --port 8001
echo.
echo Para parar:
echo   docker-compose -f docker-compose.dev.yml down
echo.
