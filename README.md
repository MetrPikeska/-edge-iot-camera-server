# 🌱 Edge IoT Camera Server

Lehký Python server pro zachycování a poskytování snímků z USB kamery. Navržen pro provoz na headless Ubuntu Server v IoT scénářích, konkrétně pro vizuální monitoring rostlin v growboxu.

## 🏗️ Architektura Systému

**Aktuální nasazení:**
- Server běží na starém notebooku s Ubuntu Server (headless)
- Umístěn v growbox skříni pro vizuální monitoring rostlin
- USB kamera (J1455) připojená na `/dev/video2`
- Zachycuje fotky/video na příkaz nebo periodicky

**Budoucí rozšíření:**
- Server bude přenesen k zákazníkovi/kamarádovi
- Bude součástí většího systému s ESP32 senzory (samostatný repozitář)
- Záznamy budou později použity pro AI modely (detekce zdraví rostlin, růstová analýza, atd.)
- Integrace s databází pro dlouhodobé ukládání dat

**Tento repozitář obsahuje:**
- Samostatný kamerový server s HTTP API
- Webové rozhraní pro live stream a snímky
- REST API pro integraci s jinými systémy
- Periodické nebo on-demand zachycování snímků

## 🎯 Features

- **USB Camera Capture**: Zachycení snímků z USB kamery (J1455) přes OpenCV s V4L2 backend
- **Live Video Stream**: Motion JPEG streaming pro sledování v reálném čase
- **HTTP Image Server**: Poskytování snímků přes HTTP přístupných z LAN
- **Web Interface**: Jednoduché webové rozhraní s živým streamem a ovládáním
- **On-Demand Capture**: Zachycení snímku na požádání přes API nebo webové tlačítko
- **Headless Operation**: Běží na Ubuntu Server bez GUI závislostí
- **Thread-Safe**: Bezpečný souběžný přístup ke kameře (streaming + capture současně)
- **REST API**: JSON endpointy pro programový přístup
- **Systemd Ready**: Navržen pro běh jako systemd služba na pozadí

## 💾 Ukládání Záznamů

**Výchozí umístění:**
- Všechny snímky se ukládají do složky `images/` v kořenovém adresáři projektu
- Cesta: `/home/metr/edge-iot-camera-server/images/`

**Aktuální soubory:**
- `snapshot.jpg` - Nejaktuálnější snímek (přepisuje se při každém zachycení)
- Přístup: `http://<server-ip>:5000/snapshot.jpg`

**Budoucí rozšíření:**
- Časové značky v názvech souborů pro historii: `20260115_143000.jpg`
- Automatické mazání starých snímků (max. 100 souborů)
- Ukládání do databáze pro long-term analýzu
- Export do cloudu nebo externího úložiště

## 📋 Requirements

### Hardware
- Ubuntu Server 24.04 (Noble) - headless bez GUI
- USB kamera J1455 (nebo jiná kompatibilní s V4L2)
- Připojeno na `/dev/video2` (metadata na `/dev/video3`)
- Síťové připojení (WiFi nebo Ethernet)
- Doporučeno: Starý notebook/miniPC pro úsporu energie

### Software
- Python 3.12 (testováno na Ubuntu 24.04)
- pip (Python package manager)
- OpenCV 4.10+ (headless verze)
- NumPy 1.26+ (kompatibilní s Python 3.12)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/MetrPikeska/edge-iot-camera-server.git
cd edge-iot-camera-server
```

### 2. Install Dependencies

```bash
# Update system packages
sudo apt update

# Install Python and required system libraries  
sudo apt install -y python3 python3-pip python3-venv

# Install OpenCV dependencies (Ubuntu 24.04)
sudo apt install -y libgl1 libglib2.0-0 libgomp1

# Install V4L utilities (optional, for diagnostics)
sudo apt install -y v4l-utils

# Create virtual environment (strongly recommended)
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install build tools
pip install --upgrade pip setuptools wheel

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Test Camera Connection

```bash
# List all video devices
ls -l /dev/video*

# Identify cameras
v4l2-ctl --list-devices

# Test USB camera (J1455 is on /dev/video2)
v4l2-ctl -d /dev/video2 --list-formats-ext

# Optional: Capture test frame with ffmpeg
sudo apt install -y ffmpeg
ffmpeg -f v4l2 -i /dev/video2 -frames:v 1 test.jpg
```

**Poznámka:** `/dev/video0` a `/dev/video1` jsou vestavěná HP kamera (pokud používáš notebook). USB kamera J1455 je na `/dev/video2`.

### 4. Start the Server

```bash
python3 app.py
```

The server will start on `http://0.0.0.0:5000`

### 5. Access from Browser

Otevři prohlížeč (např. na iPadu, mobilu, nebo PC ve stejné síti) a přejdi na:
- **Web UI s live streamem**: `http://192.168.34.11:5000/`
- **Přímý snímek**: `http://192.168.34.11:5000/snapshot.jpg`
- **Video stream**: `http://192.168.34.11:5000/video_feed`

Pro zjištění IP adresy serveru:
```bash
hostname -I
# nebo
ip addr show
```

## 📁 Project Structure

```
edge-iot-camera-server/
├── app.py                 # Flask web server (hlavní aplikace)
├── camera.py              # Modul pro práci s kamerou (OpenCV + threading)
├── config.py              # Konfigurační nastavení
├── requirements.txt       # Python závislosti
├── install.sh             # Instalační skript pro Ubuntu 24.04
├── setup_service.sh       # Skript pro systemd službu
├── test_capture.py        # Test snímání z kamery
├── README.md              # Tento soubor
├── INSTALL_CZ.md          # Instalační průvodce česky
├── QUICK_START.md         # Rychlý start guide
├── .gitignore            # Git ignore pravidla
├── images/               # Zachycené snímky (auto-vytvořeno)
│   └── snapshot.jpg      # Nejaktuálnější snímek kamery
└── venv/                 # Python virtual environment (local)
```

## 🔌 API Endpoints

### GET `/`
Webové rozhraní s live streamem a ovládáním kamery.
- **Tab "Live Stream"**: Živé video (Motion JPEG)
- **Tab "Snapshot"**: Zachycení a zobrazení snímku

### GET `/video_feed`
Vrací živý video stream ve formátu Motion JPEG.

**Použití:**
```html
<img src="http://192.168.34.11:5000/video_feed">
```

### GET `/snapshot.jpg`
Vrací nejaktuálnější zachycený snímek jako JPEG.

**Příklad:**
```bash
curl http://192.168.34.11:5000/snapshot.jpg -o latest.jpg

# Nebo ve skriptu pro periodické stahování
while true; do
  wget -O snapshot_$(date +%Y%m%d_%H%M%S).jpg http://192.168.34.11:5000/snapshot.jpg
  sleep 300  # každých 5 minut
done
```

### GET `/capture`
Spustí nové zachycení snímku z kamery (uloží jako `snapshot.jpg`).

**Response:**
```json
{
  "success": true,
  "message": "Image captured successfully",
  "timestamp": "2026-01-15T10:30:00",
  "filepath": "/home/metr/edge-iot-camera-server/images/snapshot.jpg"
}
```

**Příklad - pravidelné snímání:**
```bash
# Cron job pro snímek každou hodinu
0 * * * * curl http://localhost:5000/capture
```

### GET `/status`
Returns server status information.

**Response:**
```json
{
  "status": "online",
  "timestamp": "2026-01-15T10:30:00",
  "camera_index": 0,
  "images_dir": "/path/to/images"
}
```

### GET `/test_camera`
Tests camera connectivity.

**Response:**
```json
{
  "success": true,
  "message": "Camera test successful",
  "timestamp": "2026-01-15T10:30:00"
}
```

## ⚙️ Configuration

Edit `config.py` to customize settings:

```python
# Camera settings
CAMERA_INDEX = 2          # /dev/video2 = J1455 USB camera
CAMERA_WIDTH = 640        # Image width (max 1280 for MJPEG)
CAMERA_HEIGHT = 480       # Image height (max 720 for MJPEG)
CAMERA_FPS = 30           # Frame rate

# Server settings
HOST = '0.0.0.0'          # Listen on all interfaces
PORT = 5000               # HTTP port

# Storage settings
IMAGES_DIR = './images'   # Directory for saved images
LATEST_IMAGE_NAME = 'snapshot.jpg'  # Always overwrites
```

**Podporovaná rozlišení (J1455 USB camera):**
- YUYV: 640×480, 640×360, 424×240, 320×240, 320×180 @ 30fps
- MJPEG: až 1280×720 @ 30fps (komprimované)

## 🔧 Running as a System Service

To run the server automatically on boot, create a systemd service:

### 1. Create Service File

```bash
sudo nano /etc/systemd/system/camera-server.service
```

### 2. Add Service Configuration

```ini
[Unit]
Description=Edge IoT Camera Server
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/home/youruser/edge-iot-camera-server
Environment="PATH=/home/youruser/edge-iot-camera-server/venv/bin"
ExecStart=/home/youruser/edge-iot-camera-server/venv/bin/python3 app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable camera-server

# Start service now
sudo systemctl start camera-server

# Check status
sudo systemctl status camera-server

# View logs
sudo journalctl -u camera-server -f
```

## 🐛 Troubleshooting

### Camera Not Found

```bash
# Check if camera is connected
ls -l /dev/video*

# Test camera with v4l-utils
sudo apt install v4l-utils
v4l2-ctl --list-devices
v4l2-ctl -d /dev/video0 --all
```

### Permission Denied

```bash
# Add user to video group
sudo usermod -a -G video $USER

# Logout and login again, or run:
newgrp video
```

### OpenCV Import Error

```bash
# Install missing system dependencies
sudo apt install -y libgl1-mesa-glx libglib2.0-0
```

### Port Already in Use

```bash
# Check what's using port 5000
sudo lsof -i :5000

# Change port in config.py or kill the process
```

## 🔮 Budoucí Rozšíření

**Plánované funkce:**
- [x] Live video streaming
- [x] Thread-safe camera access
- [ ] Periodické automatické snímání (nastavitelný interval)
- [ ] Ukládání s časovými značkami (historie snímků)
- [ ] Automatické mazání starých snímků
- [ ] Integrace s ESP32 senzory přes MQTT
- [ ] Ukládání do databáze (PostgreSQL/MongoDB)
- [ ] Time-lapse video generování
- [ ] Detekce změn pohybu (motion detection)

**AI/ML funkce (budoucnost):**
- [ ] Detekce zdraví rostlin (choroby, škůdci)
- [ ] Analýza růstu a vývoje
- [ ] Automatické rozpoznávání stádia růstu
- [ ] Predikce sklizně
- [ ] Optimalizace podmínek na základě obrazu

**Integrace s growbox systémem:**
- [ ] Synchronizace s ESP32 data loggingem
- [ ] Korelace snímků s teplotou, vlhkostí, CO2
- [ ] Dashboard s metrikami a fotkami
- [ ] Notifikace při detekci problémů

## 📝 License

MIT License - feel free to use and modify for your projects.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Happy Growing! 🌱**
