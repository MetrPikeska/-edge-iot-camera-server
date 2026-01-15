"""
Configuration settings for the edge IoT camera server.
"""
import os

# Camera settings
CAMERA_INDEX = 2  # /dev/video2 = J1455 USB camera (not built-in HP camera)
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
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
