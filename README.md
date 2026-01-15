# 🌱 Edge IoT Camera Server

A lightweight Python-based edge server for capturing and serving images from a USB camera. Designed for headless Ubuntu Server deployment in IoT scenarios like plant monitoring in a growbox.

## 🎯 Features

- **USB Camera Capture**: Capture images from USB camera via `/dev/video0` using OpenCV
- **HTTP Image Server**: Serve captured images over HTTP accessible from LAN
- **Timestamp Management**: Save images with timestamps for history tracking
- **Headless Operation**: Runs on Ubuntu Server without GUI dependencies
- **Web Interface**: Simple web UI for viewing and capturing images
- **REST API**: JSON endpoints for programmatic access
- **Systemd Ready**: Designed to run as a background service

## 📋 Requirements

### Hardware
- Ubuntu Server (headless)
- USB camera connected to `/dev/video0`
- Network connection (WiFi or Ethernet)

### Software
- Python 3.8+
- pip (Python package manager)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/edge-iot-camera-server.git
cd edge-iot-camera-server
```

### 2. Install Dependencies

```bash
# Update system packages
sudo apt update

# Install Python and required system libraries
sudo apt install -y python3 python3-pip python3-venv

# Install OpenCV dependencies
sudo apt install -y libgl1-mesa-glx libglib2.0-0

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Test Camera Connection

```bash
# Test if camera is accessible
ls -l /dev/video0

# Run camera test script
python3 camera.py
```

### 4. Start the Server

```bash
python3 app.py
```

The server will start on `http://0.0.0.0:5000`

### 5. Access from Browser

Open your browser (e.g., on iPad) and navigate to:
- **Web UI**: `http://<server-ip>:5000/`
- **Direct Image**: `http://<server-ip>:5000/snapshot.jpg`

To find your server IP:
```bash
hostname -I
```

## 📁 Project Structure

```
edge-iot-camera-server/
├── app.py                 # Flask web server (main application)
├── camera.py              # Camera capture module
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── .gitignore            # Git ignore rules
├── images/               # Captured images directory (auto-created)
│   └── snapshot.jpg      # Latest camera snapshot
└── systemd/              # Systemd service files (optional)
```

## 🔌 API Endpoints

### GET `/`
Web interface for viewing and controlling the camera.

### GET `/snapshot.jpg`
Returns the latest captured image as JPEG.

**Example:**
```bash
curl http://192.168.1.100:5000/snapshot.jpg -o latest.jpg
```

### GET `/capture`
Triggers a new image capture from the camera.

**Response:**
```json
{
  "success": true,
  "message": "Image captured successfully",
  "timestamp": "2026-01-15T10:30:00",
  "filepath": "/path/to/snapshot.jpg"
}
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
CAMERA_INDEX = 0          # /dev/video0
CAMERA_WIDTH = 1920       # Image width
CAMERA_HEIGHT = 1080      # Image height

# Server settings
HOST = '0.0.0.0'          # Listen on all interfaces
PORT = 5000               # HTTP port

# Storage settings
IMAGES_DIR = './images'   # Directory for saved images
```

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

## 🔮 Future Enhancements

- [ ] Periodic automatic image capture
- [ ] MQTT integration for ESP32 sensor data
- [ ] Image history viewer
- [ ] Basic plant health detection (AI/ML)
- [ ] Multi-camera support
- [ ] Time-lapse video generation
- [ ] Mobile app integration

## 📝 License

MIT License - feel free to use and modify for your projects.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Happy Growing! 🌱**
