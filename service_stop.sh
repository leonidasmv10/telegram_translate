#!/bin/bash

# Colores para la terminal
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

clear
echo -e "${RED}==============================================${NC}"
echo -e "${CYAN}   🛑 DETENIENDO TRADUCTOR 'MAGIC SEND'       ${NC}"
echo -e "${RED}==============================================${NC}"

echo -e "\n[1/2] ${YELLOW}Apagando el motor de traducción...${NC}"
sudo systemctl stop traductor

echo -e "[2/2] ${YELLOW}Desactivando inicio automático...${NC}"
sudo systemctl disable traductor

echo -e "\n${RED}🔴 SERVICIO DESACTIVADO POR COMPLETO.${NC}"
echo -e "El bot ya no interceptará más mensajes hasta que uses ${CYAN}./service_start.sh${NC}\n"
