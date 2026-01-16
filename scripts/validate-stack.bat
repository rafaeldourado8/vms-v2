@echo off
REM Validacao rapida da stack

echo ========================================
echo GT-Vision VMS - Validacao Rapida
echo ========================================
echo.

echo [1/3] Verificando servicos Docker...
docker-compose -f docker-compose.dev.yml ps
echo.

echo [2/3] Executando smoke tests...
poetry run python tests/smoke_test.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo AVISO: Alguns servicos podem nao estar prontos
    echo Aguarde mais alguns segundos e tente novamente
    echo.
)
echo.

echo [3/3] Testando endpoints principais...
echo.
echo Streaming API Health:
curl -s http://localhost:8001/health
echo.
echo.
echo Prometheus Health:
curl -s http://localhost:9090/-/healthy
echo.
echo.
echo Grafana Health:
curl -s http://localhost:3000/api/health
echo.
echo.

echo ========================================
echo Validacao concluida!
echo ========================================
echo.
echo Acesse:
echo   Streaming API: http://localhost:8001/docs
echo   Prometheus:    http://localhost:9090
echo   Grafana:       http://localhost:3000 (admin/admin)
echo   Kibana:        http://localhost:5601
echo.
