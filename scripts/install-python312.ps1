# Instalar Python 3.12 no Windows
# Execute como Administrador

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Instalando Python 3.12" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# URL do instalador Python 3.12
$pythonUrl = "https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe"
$installerPath = "$env:TEMP\python-3.12.1-amd64.exe"

Write-Host "[1/4] Baixando Python 3.12..." -ForegroundColor Yellow
Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath

Write-Host "[2/4] Instalando Python 3.12..." -ForegroundColor Yellow
Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_test=0" -Wait

Write-Host "[3/4] Limpando arquivos temporarios..." -ForegroundColor Yellow
Remove-Item $installerPath

Write-Host "[4/4] Verificando instalacao..." -ForegroundColor Yellow
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
python --version

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Python 3.12 instalado com sucesso!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Proximos passos:" -ForegroundColor Cyan
Write-Host "1. Feche e reabra o terminal" -ForegroundColor White
Write-Host "2. Execute: python --version" -ForegroundColor White
Write-Host "3. Execute: pip install --upgrade poetry" -ForegroundColor White
Write-Host "4. Execute: poetry install" -ForegroundColor White
Write-Host ""

Read-Host "Pressione Enter para continuar"
