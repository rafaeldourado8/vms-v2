@echo off
echo ========================================
echo GT-Vision VMS - Docker Build
echo ========================================
echo.

echo [1/5] Building Detection API...
docker-compose build detection
if %errorlevel% neq 0 (
    echo ERROR: Detection build failed
    exit /b 1
)

echo.
echo [2/5] Building Backend...
docker-compose build backend
if %errorlevel% neq 0 (
    echo ERROR: Backend build failed
    exit /b 1
)

echo.
echo [3/5] Building Streaming...
docker-compose build streaming
if %errorlevel% neq 0 (
    echo ERROR: Streaming build failed
    exit /b 1
)

echo.
echo [4/5] Building Frontend...
docker-compose build frontend
if %errorlevel% neq 0 (
    echo ERROR: Frontend build failed
    exit /b 1
)

echo.
echo [5/5] Building Nginx...
docker-compose build nginx
if %errorlevel% neq 0 (
    echo ERROR: Nginx build failed
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo To start services: docker-compose up -d
echo.
