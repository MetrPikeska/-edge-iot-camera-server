# 🚀 Instalační Návod - Edge IoT Camera Server

Kompletní návod pro instalaci a nastavení na Ubuntu Server.

## 📋 Co budete potřebovat

- **Ubuntu Server** (20.04 nebo novější, testováno na 22.04)
- **USB kamera** připojená k serveru
- **SSH přístup** k serveru (nebo přímý přístup)
- **Internetové připojení** (pro stažení balíčků)

## 🎯 Rychlá instalace (Doporučeno)

### 1. SSH připojení k serveru a naklonování repozitáře

```bash
# Připojení na server
ssh uživatel@ip-serveru

# Klonování repozitáře
git clone https://github.com/tvoje-jmeno/edge-iot-camera-server.git
cd edge-iot-camera-server
```

**Alternativa:** Pokud nemáte repozitář na GitHubu, přeneste soubory:

```powershell
# Z Windows PowerShell v tomto adresáři:
scp -r * uživatel@ip-serveru:/home/uživatel/camera-server/
```

Pak:
```bash
ssh uživatel@ip-serveru
cd camera-server
```

### 2. Spusťte automatickou instalaci

```bash
# Udělat skripty spustitelné
chmod +x install.sh setup_service.sh

# Spustit instalaci
bash install.sh
```

Instalační skript automaticky:
- ✅ Aktualizuje systém
- ✅ Nainstaluje Python a závislosti
- ✅ Nastaví oprávnění pro kameru
- ✅ Vytvoří virtual environment
- ✅ Nainstaluje Python balíčky
- ✅ Zkontroluje kameru

### 3. DŮLEŽITÉ: Odhlaste se a znovu přihlaste

```bash
exit  # Ukončit SSH
ssh uživatel@ip-serveru  # Znovu se připojit
cd edge-iot-camera-server
```

Nebo jednoduše:

```bash
newgrp video
```

### 4. Test kamery

```bash
source venv/bin/activate
python3 test_capture.py
```

Pokud test projde úspěšně, měli byste vidět:
```
✓ PASSED: Camera is accessible
✓ PASSED: Image captured successfully
```

### 5. Spuštění serveru (manuálně)

```bash
source venv/bin/activate
python3 app.py
```

Server poběží na `http://<ip-serveru>:5000/`

Pro ukončení: `Ctrl+C`

### 6. Nastavení automatického startu (doporučeno)

```bash
bash setup_service.sh
```

Služba se nyní spustí automaticky při každém startu systému.

---

## 🔄 Aktualizace kódu (pull z GitHubu)

Když provedete změny v kódu a pushete na GitHub:

```bash
# Na serveru
cd edge-iot-camera-server
git pull

# Restart služby, pokud běží
sudo systemctl restart camera-server
```

## 📱 Přístup k serveru

### Z webového prohlížeče (iPad, mobil, PC):

- **Web rozhraní**: `http://<ip-serveru>:5000/`
- **Přímý odkaz na obrázek**: `http://<ip-serveru>:5000/snapshot.jpg`

### Zjištění IP adresy serveru:

```bash
hostname -I
```

Nebo:

```bash
ip addr show
```

## 🔧 Ruční instalace (krok za krokem)

Pokud preferujete manuální instalaci nebo instalační skript nefunguje:

### 1. Aktualizace systému

```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Instalace Python a závislostí

```bash
sudo apt install -y python3 python3-pip python3-venv
sudo apt install -y libgl1-mesa-glx libglib2.0-0 v4l-utils
```

### 3. Oprávnění pro kameru

```bash
# Přidat uživatele do skupiny video
sudo usermod -a -G video $USER

# Odhlásit se a znovu přihlásit
exit
ssh uživatel@ip-serveru
```

### 4. Kontrola kamery

```bash
# Zkontrolovat, zda kamera existuje
ls -l /dev/video0

# Informace o kameře
v4l2-ctl -d /dev/video0 --all
```

### 5. Nastavení projektu

```bash
cd /home/uživatel/camera-server

# Vytvořit virtual environment
python3 -m venv venv

# Aktivovat virtual environment
source venv/bin/activate

# Nainstalovat závislosti
pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Test

```bash
python3 test_capture.py
```

### 7. Spuštění

```bash
python3 app.py
```

## 🛠️ Správa služby (po nastavení systemd)

### Zobrazit status

```bash
sudo systemctl status camera-server
```

### Zobrazit logy v reálném čase

```bash
sudo journalctl -u camera-server -f
```

### Restart služby

```bash
sudo systemctl restart camera-server
```

### Zastavit službu

```bash
sudo systemctl stop camera-server
```

### Spustit službu

```bash
sudo systemctl start camera-server
```

### Zakázat automatický start

```bash
sudo systemctl disable camera-server
```

### Povolit automatický start

```bash
sudo systemctl enable camera-server
```

## 🐛 Řešení problémů

### Kamera nenalezena

```bash
# Zkontrolovat připojená USB zařízení
lsusb

# Zkontrolovat video zařízení
ls -l /dev/video*

# Informace o kameře
v4l2-ctl --list-devices
```

### Oprávnění odmítnuta

```bash
# Zkontrolovat skupiny uživatele
groups

# Měli byste vidět "video" ve výstupu
# Pokud ne, přidejte se znovu:
sudo usermod -a -G video $USER

# A odhlaste se / přihlaste se znovu
```

### Port 5000 je obsazený

```bash
# Zjistit, co používá port 5000
sudo lsof -i :5000

# Změnit port v config.py
nano config.py
# Změňte: PORT = 8080  # nebo jiný volný port
```

### OpenCV chyba

```bash
# Reinstalovat systemové závislosti
sudo apt install -y libgl1-mesa-glx libglib2.0-0

# Reinstalovat opencv v virtual environment
source venv/bin/activate
pip uninstall opencv-python-headless
pip install opencv-python-headless
```

### Server není dostupný z jiného zařízení

```bash
# Zkontrolovat firewall
sudo ufw status

# Povolit port 5000
sudo ufw allow 5000

# Nebo vypnout firewall (pouze pro testování!)
sudo ufw disable
```

### Služba se nespustí po restartu

```bash
# Zkontrolovat logy
sudo journalctl -u camera-server -n 50

# Zkontrolovat status
sudo systemctl status camera-server

# Restartovat službu
sudo systemctl restart camera-server
```

## 📊 Testování z jiného zařízení

### Z Windows (PowerShell):

```powershell
# Stáhnout obrázek
Invoke-WebRequest -Uri "http://192.168.1.100:5000/snapshot.jpg" -OutFile "snapshot.jpg"

# Test API
Invoke-WebRequest -Uri "http://192.168.1.100:5000/status"
```

### Z Linuxu/macOS:

```bash
# Stáhnout obrázek
curl http://192.168.1.100:5000/snapshot.jpg -o snapshot.jpg

# Test API
curl http://192.168.1.100:5000/status
```

### Z prohlížeče:

Jednoduše otevřete: `http://<ip-serveru>:5000/`

## 🔒 Bezpečnostní tipy (Produkce)

1. **Změňte výchozí port** (pokud je 5000 příliš běžný)
2. **Nastavte firewall** - povolte pouze potřebné porty
3. **Používejte reverse proxy** (nginx) s SSL
4. **Omezte přístup** pouze na lokální síť
5. **Pravidelně aktualizujte** systém a závislosti

## 📝 Poznámky

- Server běží na **všech síťových rozhraních** (0.0.0.0)
- Obrázky se ukládají do adresáře `images/`
- Nejnovější obrázek je vždy `images/snapshot.jpg`
- Historické obrázky mají timestamp ve jméně

## 🎉 Hotovo!

Server je nyní připraven a můžete sledovat svůj growbox odkudkoliv v lokální síti!

---

**Potřebujete pomoc?** Otevřete issue na GitHubu.
