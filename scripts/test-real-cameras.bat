@echo off
echo ========================================
echo GT-Vision VMS - Teste Cameras REAIS
echo ========================================
echo.
echo Cameras:
echo   1. 45.236.226.75:6052
echo   2. 45.236.226.74:6050
echo   3. 45.236.226.72:6048
echo   4. 45.236.226.71:6047
echo   5. 45.236.226.71:6046
echo.
echo Executando teste...
echo.
python scripts\test_real_cameras.py
echo.
pause
