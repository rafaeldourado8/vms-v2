@echo off
echo ========================================
echo GT-Vision VMS - Stack Completa
echo HAProxy + Kong + Todos os Servicos
echo ========================================
echo.

echo [1/4] Parando servicos antigos...
docker-compose down
echo.

echo [2/4] Iniciando stack completa...
docker-compose -f docker-compose.full.yml up -d
echo.

echo Aguardando servicos (60s)...
timeout /t 60 /nobreak
echo.

echo [3/4] Verificando status...
docker-compose -f docker-compose.full.yml ps
echo.

echo [4/4] Testando endpoints...
echo.
echo HAProxy Stats:
curl -s http://localhost:8404/stats | findstr "HAProxy"
echo.
echo.
echo Kong Health:
curl -s http://localhost:8000
echo.
echo.
echo Streaming via HAProxy:
curl -s http://localhost/api/streaming/health
echo.
echo.

echo ========================================
echo Stack Completa Rodando!
echo ========================================
echo.
echo Endpoints:
echo   HAProxy:       http://localhost
echo   HAProxy Stats: http://localhost:8404/stats
echo   Kong:          http://localhost:8000
echo   Streaming:     http://localhost:8001/health
echo   Prometheus:    http://localhost:9090
echo   Grafana:       http://localhost:3000
echo.
echo Para parar:
echo   docker-compose -f docker-compose.full.yml down
echo.
