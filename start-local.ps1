# Script para iniciar la aplicación Flask de Kahoot localmente
# Uso: .\start-local.ps1

Write-Host "🚀 Iniciando Kitty Tools - Kahoot Application" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
$kahootDir = "C:\Users\usuario\Documents\GitHub\jeko1107.github.io\kahoot"
if (-not (Test-Path $kahootDir)) {
    Write-Host "❌ Error: No se encuentra el directorio kahoot" -ForegroundColor Red
    exit 1
}

Set-Location $kahootDir

# Verificar Python
Write-Host "📦 Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "   Descarga Python desde: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Instalar dependencias si es necesario
Write-Host ""
Write-Host "📦 Instalando/Verificando dependencias..." -ForegroundColor Yellow
$requirementsFile = ".\webapp\requirements.txt"

if (Test-Path $requirementsFile) {
    pip install -r $requirementsFile --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Dependencias instaladas correctamente" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Advertencia: Algunas dependencias podrían no haberse instalado" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  No se encontró requirements.txt, instalando dependencias básicas..." -ForegroundColor Yellow
    pip install flask colorama pystyle --quiet
}

# Configurar variables de entorno
Write-Host ""
Write-Host "🔧 Configurando variables de entorno..." -ForegroundColor Yellow
$env:KITTY_WEB_SECRET = "dev-secret-key-$(Get-Random)"
$env:KITTY_WEB_USER = "admin"
$env:KITTY_WEB_PASS = "admin"

Write-Host "✅ Usuario: admin" -ForegroundColor Green
Write-Host "✅ Password: admin" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  IMPORTANTE: Cambia estas credenciales en producción!" -ForegroundColor Yellow

# Iniciar la aplicación
Write-Host ""
Write-Host "🌐 Iniciando servidor Flask..." -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 La aplicación estará disponible en:" -ForegroundColor Green
Write-Host "   http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Para detener el servidor, presiona Ctrl+C" -ForegroundColor Yellow
Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

Set-Location ".\webapp"

# Iniciar Flask
python app.py
