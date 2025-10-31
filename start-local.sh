#!/bin/bash
# Script para iniciar la aplicación Flask de Kahoot localmente
# Uso: ./start-local.sh

echo "🚀 Iniciando Kitty Tools - Kahoot Application"
echo "============================================="
echo ""

# Verificar que estamos en el directorio correcto
KAHOOT_DIR="kahoot"
if [ ! -d "$KAHOOT_DIR" ]; then
    echo "❌ Error: No se encuentra el directorio kahoot"
    exit 1
fi

cd "$KAHOOT_DIR"

# Verificar Python
echo "📦 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ Python encontrado: $PYTHON_VERSION"

# Instalar dependencias si es necesario
echo ""
echo "📦 Instalando/Verificando dependencias..."
REQUIREMENTS_FILE="./webapp/requirements.txt"

if [ -f "$REQUIREMENTS_FILE" ]; then
    pip3 install -r "$REQUIREMENTS_FILE" --quiet
    echo "✅ Dependencias instaladas correctamente"
else
    echo "⚠️  No se encontró requirements.txt, instalando dependencias básicas..."
    pip3 install flask colorama pystyle --quiet
fi

# Configurar variables de entorno
echo ""
echo "🔧 Configurando variables de entorno..."
export KITTY_WEB_SECRET="dev-secret-key-$RANDOM"
export KITTY_WEB_USER="admin"
export KITTY_WEB_PASS="admin"

echo "✅ Usuario: admin"
echo "✅ Password: admin"
echo ""
echo "⚠️  IMPORTANTE: Cambia estas credenciales en producción!"

# Iniciar la aplicación
echo ""
echo "🌐 Iniciando servidor Flask..."
echo "============================================="
echo ""
echo "📍 La aplicación estará disponible en:"
echo "   http://127.0.0.1:5000"
echo ""
echo "💡 Para detener el servidor, presiona Ctrl+C"
echo ""
echo "============================================="
echo ""

cd webapp
python3 app.py
