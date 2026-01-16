@echo off
echo ========================================
echo Sprint 13 - Teste de Autenticacao JWT
echo ========================================
echo.

cd ..

echo [1/4] Rebuild do container streaming...
docker-compose -f docker-compose.dev.yml build streaming
if %errorlevel% neq 0 (
    echo ERRO: Falha no build
    exit /b 1
)

echo.
echo [2/4] Restart do container...
docker-compose -f docker-compose.dev.yml up -d streaming
if %errorlevel% neq 0 (
    echo ERRO: Falha ao iniciar
    exit /b 1
)

echo.
echo [3/4] Aguardando API iniciar (10s)...
timeout /t 10 /nobreak > nul

echo.
echo [4/4] Testando endpoints de autenticacao...
echo.

echo --- Health Check ---
curl -s http://localhost:8001/health
echo.
echo.

echo --- Login (admin@gtvision.com.br / admin123) ---
curl -s -X POST http://localhost:8001/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"admin@gtvision.com.br\",\"password\":\"admin123\"}" > token.json
type token.json
echo.
echo.

echo --- Extraindo token ---
for /f "tokens=2 delims=:," %%a in ('type token.json ^| findstr "access_token"') do set TOKEN=%%a
set TOKEN=%TOKEN:"=%
set TOKEN=%TOKEN: =%
echo Token: %TOKEN:~0,50%...
echo.

echo --- GET /api/auth/me (autenticado) ---
curl -s http://localhost:8001/api/auth/me ^
  -H "Authorization: Bearer %TOKEN%"
echo.
echo.

echo --- GET /api/auth/me (sem token - deve falhar) ---
curl -s http://localhost:8001/api/auth/me
echo.
echo.

echo --- Swagger UI ---
echo Acesse: http://localhost:8001/docs
echo.

echo ========================================
echo Teste concluido!
echo ========================================
del token.json 2>nul
