#!/bin/bash

# Script de inicio para Ubuntu/Linux
echo "=============================================="
echo "   Iniciando Traductor Magic Send (Linux)"
echo "=============================================="

# 1. Crear entorno virtual si no existe
if [ ! -d ".venv" ]; then
    echo "[INFO] Creando entorno virtual..."
    python3 -m venv .venv
fi

# 2. Activar entorno virtual
source .venv/bin/activate

# 3. Instalar/Actualizar dependencias
echo "[INFO] Verificando dependencias..."
pip install -r requirements.txt -q

# 4. Comprobar sesión y arrancar
if [ ! -f "mi_sesion.session" ]; then
    echo "[ALERTA] Sesión de Telegram no encontrada."
    echo "Ejecuta: python3 login.py  para autorizar tu cuenta."
else
    echo "[INFO] Lanzando interceptor..."
    python3 main.py
fi
