@echo off
echo ========================================
echo GT-Vision VMS - Streaming Service Test
echo ========================================
echo.

echo [1/5] Building containers...
docker-compose -f docker-compose.test.yml build

echo.
echo [2/5] Starting services...
docker-compose -f docker-compose.test.yml up -d

echo.
echo [3/5] Waiting for services to be ready...
timeout /t 10 /nobreak

echo.
echo [4/5] Testing MediaMTX API...
curl -s http://localhost:9997/v3/config/global/get

echo.
echo.
echo [5/5] Testing Streaming API...
curl -s http://localhost:8001/health

echo.
echo.
echo ========================================
echo Services Status:
echo ========================================
docker-compose -f docker-compose.test.yml ps

echo.
echo ========================================
echo Test URLs:
echo ========================================
echo MediaMTX API:    http://localhost:9997
echo Streaming API:   http://localhost:8001
echo Health Check:    http://localhost:8001/health
echo API Docs:        http://localhost:8001/docs
echo.
echo ========================================
echo To test stream start:
echo ========================================
echo curl -X POST http://localhost:8001/api/streams/start \
echo   -H "Content-Type: application/json" \
echo   -d "{\"camera_id\":\"123e4567-e89b-12d3-a456-426614174000\",\"source_url\":\"rtsp://test\"}"
echo.
echo ========================================
echo To stop services:
echo ========================================
echo docker-compose -f docker-compose.test.yml down
echo.
