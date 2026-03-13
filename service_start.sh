#!/bin/bash

# Colores para la terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

clear
echo -e "${BLUE}==============================================${NC}"
echo -e "${CYAN}   🚀 INICIANDO TRADUCTOR 'MAGIC SEND' 24/7   ${NC}"
echo -e "${BLUE}==============================================${NC}"

# 1. Configuración de archivos
echo -e "\n[1/3] ${YELLOW}Configurando archivos de sistema...${NC}"
sudo cp traductor.service /etc/systemd/system/
sudo systemctl daemon-reload

# 2. Activación del servicio
echo -e "[2/3] ${YELLOW}Activando el servicio en segundo plano...${NC}"
sudo systemctl enable traductor
sudo systemctl start traductor

# 3. Verificación final
echo -e "[3/3] ${YELLOW}Verificando estado...${NC}"
sleep 2

STATUS=$(sudo systemctl is-active traductor)

if [ "$STATUS" = "active" ]; then
    echo -e "\n${GREEN}✅ ¡TODO LISTO! El traductor está OPERATIVO.${NC}"
    echo -e "${CYAN}----------------------------------------------${NC}"
    echo -e "📱 Chat objetivo: ${YELLOW}Configurado en config.ini${NC}"
    echo -e "🏠 Directorio: ${BLUE}$(pwd)${NC}"
    echo -e "📡 Servicio: ${GREEN}Activo (Perpetuo)${NC}"
    echo -e "${CYAN}----------------------------------------------${NC}"
    echo -e "\n${BLUE}💡 TIP:${NC} Para ver qué está pasando en vivo, usa:"
    echo -e "${YELLOW}   sudo journalctl -u traductor -f${NC}\n"
else
    echo -e "\n${NC}❌ ${YELLOW}ALERTA:${NC} El servicio no arrancó correctamente."
    echo -e "Usa 'sudo systemctl status traductor' para ver el error."
fi
