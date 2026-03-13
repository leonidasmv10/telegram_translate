#!/bin/bash

# Script para arrancar el servicio de forma permanente
echo "[INFO] Iniciando el servicio de traducción 24/7..."

# Aseguramos permisos y copiamos el servicio
sudo cp traductor.service /etc/systemd/system/
sudo systemctl daemon-reload

# Habilitamos y arrancamos
sudo systemctl enable traductor
sudo systemctl start traductor

echo "✅ Servicio ACTIVADO."
echo "Puedes ver el estado con: sudo systemctl status traductor"
