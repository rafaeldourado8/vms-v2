@echo off
REM ============================================
REM Gerar Evidencias de Autoria
REM ============================================

echo.
echo ========================================
echo   Gerando Evidencias de Autoria
echo ========================================
echo.

set DATA=%date:~-4%-%date:~3,2%-%date:~0,2%
set HORA=%time:~0,2%-%time:~3,2%-%time:~6,2%
set ARQUIVO=evidencias\autoria_%DATA%_%HORA%.txt

REM Criar pasta de evidencias
if not exist evidencias mkdir evidencias

echo Gerando relatorio de autoria...
echo.

REM Gerar relatorio
(
echo ============================================
echo EVIDENCIA DE AUTORIA - GT-VISION VMS
echo ============================================
echo.
echo Data: %date% %time%
echo Autor: Rafael Dourado Crispim
echo Email: rafaeldouradoc7@gmail.com
echo.
echo ============================================
echo ESTATISTICAS DO PROJETO
echo ============================================
echo.

REM Contar arquivos
echo [Arquivos Python]
dir /s /b src\*.py 2^>nul | find /c ".py"

echo.
echo [Total de Arquivos]
dir /s /b src\* 2^>nul | find /c "\"

echo.
echo ============================================
echo HISTORICO GIT
echo ============================================
echo.

REM Historico de commits
git rev-parse HEAD >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Nenhum commit encontrado! Execute: scripts\commit-today.bat
) else (
    git log --all --oneline --no-merges
)

echo.
echo ============================================
echo AUTORIA POR ARQUIVO
echo ============================================
echo.

REM Autoria detalhada
git rev-parse HEAD >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Execute os commits primeiro!
) else (
    git log --all -10 --pretty=format:"%%h - %%an - %%ad - %%s" --date=short
)

echo.
echo ============================================
echo LINHAS DE CODIGO
echo ============================================
echo.

REM Contar linhas (aproximado)
git ls-files src\*.py 2^>nul | find /c ".py"

echo.
echo ============================================
echo ASSINATURA DIGITAL
echo ============================================
echo.
echo Autor: Rafael Dourado Crispim
echo CPF: [INSERIR CPF]
echo Data: %date%
echo Hash do Repositorio:
git rev-parse HEAD

echo.
echo ============================================
echo DECLARACAO
echo ============================================
echo.
echo Declaro que sou o unico autor e desenvolvedor
echo do software GT-Vision VMS, tendo criado todo
echo o codigo, arquitetura e documentacao.
echo.
echo Todos os direitos reservados conforme
echo Lei 9.609/98 e Lei 9.610/98.
echo.
echo _________________________________
echo Rafael Dourado Crispim
echo.

) > "%ARQUIVO%"

echo Relatorio gerado: %ARQUIVO%
echo.

REM Gerar hash do codigo
echo Gerando hash SHA256 do codigo...
certutil -hashfile "%ARQUIVO%" SHA256 > "%ARQUIVO%.sha256"

echo Hash gerado: %ARQUIVO%.sha256
echo.

REM Criar ZIP com timestamp
echo Criando backup com timestamp...
set ZIPFILE=evidencias\codigo_fonte_%DATA%_%HORA%.zip
powershell Compress-Archive -Path src\*,LICENSE,AUTORIA.md,README.md -DestinationPath "%ZIPFILE%" -Force

echo Backup criado: %ZIPFILE%
echo.

echo ========================================
echo   Evidencias geradas com sucesso!
echo ========================================
echo.
echo Arquivos criados:
echo   1. %ARQUIVO%
echo   2. %ARQUIVO%.sha256
echo   3. %ZIPFILE%
echo.
echo IMPORTANTE:
echo   - Envie estes arquivos para seu email
echo   - Guarde em 3 locais diferentes
echo   - Nao modifique os arquivos
echo   - Timestamps provam autoria
echo.
pause
