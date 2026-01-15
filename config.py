"""
Configuration settings for the edge IoT camera server.
"""
import os

# Camera settings
CAMERA_INDEX = 0  # /dev/video0 on Linux
CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080
CAMERA_FPS = 30

# Image storage settings
IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'images')
LATEST_IMAGE_NAME = 'snapshot.jpg'
TIMESTAMP_FORMAT = '%Y%m%d_%H%M%S'

# Web server settings
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 5000
DEBUG = False  # Set to True only during development

# Future settings (for periodic capture)
CAPTURE_INTERVAL_SECONDS = 300  # 5 minutes
MAX_STORED_IMAGES = 100  # Maximum number of historical images to keep
