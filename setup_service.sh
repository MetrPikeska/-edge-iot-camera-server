#!/bin/bash
# Skript pro nastavení systemd služby
# Použití: bash setup_service.sh

set -e

echo "=========================================="
echo "Nastavení systemd služby"
echo "=========================================="
echo ""

# Barvy
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Kontrola, že skript není spuštěn jako root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}✗ Nespouštějte tento skript jako root!${NC}"
    exit 1
fi

# Získání cest
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
USER_NAME=$(whoami)
VENV_PYTHON="$SCRIPT_DIR/venv/bin/python3"

echo -e "${YELLOW}Pracovní adresář:${NC} $SCRIPT_DIR"
echo -e "${YELLOW}Uživatel:${NC} $USER_NAME"
echo ""

# Kontrola, že existuje venv
if [ ! -f "$VENV_PYTHON" ]; then
    echo -e "${RED}✗ Virtual environment nenalezen!${NC}"
    echo "  Nejprve spusťte: bash install.sh"
    exit 1
fi

# Vytvoření systemd service souboru
SERVICE_FILE="/tmp/camera-server.service"

cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Edge IoT Camera Server
After=network.target

[Service]
Type=simple
User=$USER_NAME
WorkingDirectory=$SCRIPT_DIR
Environment="PATH=$SCRIPT_DIR/venv/bin"
ExecStart=$VENV_PYTHON app.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo -e "${GREEN}✓ Service soubor vytvořen${NC}"
echo ""

# Instalace service
echo -e "${YELLOW}Instalace systemd služby...${NC}"
sudo cp "$SERVICE_FILE" /etc/systemd/system/camera-server.service
sudo systemctl daemon-reload
echo -e "${GREEN}✓ Služba nainstalována${NC}"
echo ""

# Povolení služby
echo -e "${YELLOW}Povolení automatického startu...${NC}"
sudo systemctl enable camera-server.service
echo -e "${GREEN}✓ Automatický start povolen${NC}"
echo ""

# Spuštění služby
echo -e "${YELLOW}Spouštění služby...${NC}"
sudo systemctl start camera-server.service
echo -e "${GREEN}✓ Služba spuštěna${NC}"
echo ""

# Kontrola stavu
sleep 2
echo "=========================================="
echo "Status služby:"
echo "=========================================="
sudo systemctl status camera-server.service --no-pager
echo ""

# Zjištění IP adresy
IP_ADDR=$(hostname -I | awk '{print $1}')

echo "=========================================="
echo "Hotovo!"
echo "=========================================="
echo ""
echo "Služba je nyní aktivní a spustí se automaticky při startu systému."
echo ""
echo "Užitečné příkazy:"
echo ""
echo "  ${YELLOW}Zobrazit status:${NC}"
echo "    sudo systemctl status camera-server"
echo ""
echo "  ${YELLOW}Zobrazit logy:${NC}"
echo "    sudo journalctl -u camera-server -f"
echo ""
echo "  ${YELLOW}Restart služby:${NC}"
echo "    sudo systemctl restart camera-server"
echo ""
echo "  ${YELLOW}Zastavit službu:${NC}"
echo "    sudo systemctl stop camera-server"
echo ""
echo "  ${YELLOW}Zakázat automatický start:${NC}"
echo "    sudo systemctl disable camera-server"
echo ""
echo "Přístup z prohlížeče:"
echo "  http://$IP_ADDR:5000/"
echo ""
echo "=========================================="
