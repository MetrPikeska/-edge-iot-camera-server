# ⚡ Rychlý Start

## Pro ty, kteří chtějí začít RYCHLE

### 1️⃣ SSH na server a naklonuj repozitář

```bash
ssh uživatel@ip-serveru
git clone https://github.com/tvoje-jmeno/edge-iot-camera-server.git
cd edge-iot-camera-server
```

**Nebo** pokud nemáš repozitář na GitHubu, přenes soubory:
```bash
# Z Windows PowerShell:
scp -r * uživatel@ip-serveru:/home/uživatel/camera-server/
# Pak:
ssh uživatel@ip-serveru
cd camera-server
```

### 2️⃣ Instalace

```bash
chmod +x install.sh setup_service.sh
bash install.sh
```

### 3️⃣ Odhlásit a znovu přihlásit

```bash
exit
ssh uživatel@ip-serveru
cd edge-iot-camera-server
```

### 4️⃣ Test

```bash
source venv/bin/activate
python3 test_capture.py
```

### 5️⃣ Spuštění

**Manuální** (pro testování):
```bash
python3 app.py
```

**Automatický** (běží na pozadí, start při bootu):
```bash
bash setup_service.sh
```

### 6️⃣ Přístup

Otevřete v prohlížeči:
```
http://<ip-serveru>:5000/
```

---

## 🔧 Užitečné příkazy

```bash
# Zjistit IP serveru
hostname -I

# Zobrazit logy služby
sudo journalctl -u camera-server -f

# Restart služby
sudo systemctl restart camera-server

# Test kamery
ls -l /dev/video0
v4l2-ctl -d /dev/video0 --info
```

---

**To je vše!** 🎉
