#!/bin/bash

# Script para detener el servicio de traducción
echo "[INFO] Deteniendo el servicio de traducción..."

sudo systemctl stop traductor
sudo systemctl disable traductor

echo "🛑 Servicio DESACTIVADO."
