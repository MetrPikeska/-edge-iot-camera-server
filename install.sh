#!/bin/bash
# Instalační skript pro Edge IoT Camera Server
# Použití: bash install.sh

set -e  # Ukončit při chybě

echo "=========================================="
echo "Edge IoT Camera Server - Instalace"
echo "=========================================="
echo ""

# Barvy pro výstup
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Kontrola, že skript není spuštěn jako root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}✗ Nespouštějte tento skript jako root!${NC}"
    echo "  Spusťte: bash install.sh"
    exit 1
fi

# Detekce pracovního adresáře
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo -e "${YELLOW}Pracovní adresář:${NC} $SCRIPT_DIR"
echo ""

# Krok 1: Update systému
echo -e "${YELLOW}[1/6] Aktualizace systému...${NC}"
sudo apt update
echo -e "${GREEN}✓ Hotovo${NC}"
echo ""

# Krok 2: Instalace Python a závislostí
echo -e "${YELLOW}[2/6] Instalace Python a systémových závislostí...${NC}"
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    libgl1 \
    libglib2.0-0 \
    v4l-utils \
    libgomp1
echo -e "${GREEN}✓ Hotovo${NC}"
echo ""

# Krok 3: Přidání uživatele do video skupiny
echo -e "${YELLOW}[3/6] Nastavení oprávnění pro kameru...${NC}"
sudo usermod -a -G video $USER
echo -e "${GREEN}✓ Uživatel $USER přidán do skupiny 'video'${NC}"
echo -e "${YELLOW}  Poznámka: Musíte se odhlásit a znovu přihlásit, aby se změny projevily${NC}"
echo ""

# Krok 4: Vytvoření virtual environment
echo -e "${YELLOW}[4/6] Vytváření Python virtual environment...${NC}"
cd "$SCRIPT_DIR"
python3 -m venv venv
echo -e "${GREEN}✓ Virtual environment vytvořen${NC}"
echo ""

# Krok 5: Instalace Python balíčků
echo -e "${YELLOW}[5/6] Instalace Python balíčků...${NC}"
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
echo -e "${GREEN}✓ Python balíčky nainstalovány${NC}"
echo ""

# Krok 6: Vytvoření adresáře pro obrázky
echo -e "${YELLOW}[6/6] Vytváření adresáře pro obrázky...${NC}"
mkdir -p images
echo -e "${GREEN}✓ Adresář vytvořen${NC}"
echo ""

# Test kamery
echo "=========================================="
echo "Test kamery"
echo "=========================================="
echo ""

if [ -e /dev/video0 ]; then
    echo -e "${GREEN}✓ Kamera nalezena: /dev/video0${NC}"
    echo ""
    echo "Informace o kameře:"
    v4l2-ctl -d /dev/video0 --info 2>/dev/null || echo "  (nelze získat detaily)"
else
    echo -e "${RED}✗ Kamera nenalezena na /dev/video0${NC}"
    echo "  Zkontrolujte připojení USB kamery"
fi
echo ""

# Zjištění IP adresy
echo "=========================================="
echo "Síťové informace"
echo "=========================================="
echo ""
IP_ADDR=$(hostname -I | awk '{print $1}')
echo -e "${GREEN}IP adresa serveru:${NC} $IP_ADDR"
echo ""

# Souhrn
echo "=========================================="
echo "Instalace dokončena!"
echo "=========================================="
echo ""
echo "Další kroky:"
echo ""
echo "1. ${YELLOW}ODHLASTE SE A ZNOVU SE PŘIHLASTE${NC}"
echo "   (nebo spusťte: newgrp video)"
echo ""
echo "2. Test kamery:"
echo "   cd $SCRIPT_DIR"
echo "   source venv/bin/activate"
echo "   python3 test_capture.py"
echo ""
echo "3. Spuštění serveru:"
echo "   python3 app.py"
echo ""
echo "4. Přístup z prohlížeče:"
echo "   http://$IP_ADDR:5000/"
echo "   http://$IP_ADDR:5000/snapshot.jpg"
echo ""
echo "5. Pro automatické spuštění při startu:"
echo "   bash setup_service.sh"
echo ""
echo "=========================================="
