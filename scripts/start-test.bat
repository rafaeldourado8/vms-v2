@echo off
echo ========================================
echo GT-Vision VMS - Ambiente de Testes
echo HAProxy + Kong + Stack Completa
echo ========================================
echo.

echo [1/3] Parando ambiente dev...
docker-compose -f docker-compose.dev.yml down
echo.

echo [2/3] Iniciando ambiente de testes...
docker-compose -f docker-compose.test.yml up -d
echo.

echo Aguardando servicos (60s)...
timeout /t 60 /nobreak
echo.

echo [3/3] Validando servicos...
docker-compose -f docker-compose.test.yml ps
echo.

echo ========================================
echo Ambiente de Testes Pronto!
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
echo Testar:
echo   curl http://localhost:8404/stats
echo   curl http://localhost:8000
echo   curl http://localhost/api/streaming/health
echo.
echo Para parar:
echo   docker-compose -f docker-compose.test.yml down
echo.
