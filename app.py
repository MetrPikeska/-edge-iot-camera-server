"""
Flask web server for edge IoT camera system.
Provides HTTP endpoints to capture and serve camera images.
"""
import os
import logging
from flask import Flask, send_file, jsonify, render_template_string, Response
from datetime import datetime
import config
from camera import CameraCapture, capture_snapshot

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize camera
camera = CameraCapture()


# Simple HTML template for the index page
INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Edge IoT Camera Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            border-bottom: 2px solid #ddd;
        }
        .tab {
            padding: 10px 20px;
            cursor: pointer;
            background: none;
            border: none;
            border-bottom: 3px solid transparent;
            font-size: 16px;
            color: #666;
        }
        .tab.active {
            color: #4CAF50;
            border-bottom-color: #4CAF50;
            font-weight: bold;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        .image-container {
            text-align: center;
            margin: 20px 0;
        }
        img, .stream-container {
            max-width: 100%;
            height: auto;
            border: 2px solid #ddd;
            border-radius: 4px;
        }
        .stream-container {
            background: #000;
            min-height: 480px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .stream-container img {
            border: none;
            max-height: 720px;
        }
        .button {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 12px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px 2px;
            cursor: pointer;
            border-radius: 4px;
        }
        .button:hover {
            background-color: #45a049;
        }
        .button.secondary {
            background-color: #2196F3;
        }
        .button.secondary:hover {
            background-color: #0b7dda;
        }
        .info {
            background-color: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 12px;
            margin: 10px 0;
        }
        .timestamp {
            color: #666;
            font-size: 14px;
        }
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background-color: #4CAF50;
            margin-right: 5px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌱 Edge IoT Camera Server</h1>
        
        <div class="info">
            <span class="status-indicator"></span>
            <strong>Status:</strong> {{ status }}<br>
            <strong>Last Update:</strong> <span class="timestamp">{{ timestamp }}</span>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="switchTab('live')">📹 Live Stream</button>
            <button class="tab" onclick="switchTab('snapshot')">📸 Snapshot</button>
        </div>
        
        <!-- Live Stream Tab -->
        <div id="live-tab" class="tab-content active">
            <h2>Live Video Stream</h2>
            <div class="stream-container">
                <img src="/video_feed" alt="Live camera stream">
            </div>
            <p style="color: #666; text-align: center;">
                <small>Motion JPEG stream - updates automatically</small>
            </p>
        </div>
        
        <!-- Snapshot Tab -->
        <div id="snapshot-tab" class="tab-content">
            <h2>Latest Snapshot</h2>
            <div>
                <button class="button" onclick="captureImage()">📸 Capture New Image</button>
                <button class="button secondary" onclick="refreshImage()">🔄 Refresh View</button>
            </div>
            
            <div class="image-container">
                <img id="snapshot" src="/snapshot.jpg?t={{ cache_bust }}" alt="Latest camera snapshot">
            </div>
        </div>
        
        <div class="info">
            <strong>Direct URLs:</strong><br>
            Live stream: <code>http://{{ host }}:{{ port }}/video_feed</code><br>
            Latest snapshot: <code>http://{{ host }}:{{ port }}/snapshot.jpg</code>
        </div>
    </div>
    
    <script>
        function switchTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(el => {
                el.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(el => {
                el.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName + '-tab').classList.add('active');
            event.target.classList.add('active');
        }
        
        function refreshImage() {
            const img = document.getElementById('snapshot');
            img.src = '/snapshot.jpg?t=' + new Date().getTime();
        }
        
        async function captureImage() {
            try {
                const response = await fetch('/capture');
                const data = await response.json();
                
                if (data.success) {
                    alert('✓ Image captured successfully!');
                    refreshImage();
                } else {
                    alert('✗ Failed to capture image: ' + (data.error || 'Unknown error'));
                }
            } catch (error) {
                alert('✗ Error: ' + error.message);
            }
        }
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """
    Main page with live camera view and controls.
    """
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    return render_template_string(
        INDEX_HTML,
        status="Online",
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        cache_bust=int(datetime.now().timestamp()),
        host=local_ip,
        port=config.PORT
    )


@app.route('/snapshot.jpg')
def get_snapshot():
    """
    Serve the latest captured image.
    
    Returns:
        JPEG image file
    """
    snapshot_path = os.path.join(config.IMAGES_DIR, config.LATEST_IMAGE_NAME)
    
    # Check if snapshot exists
    if not os.path.exists(snapshot_path):
        logger.warning("Snapshot not found, capturing new image...")
        success, _ = capture_snapshot()
        
        if not success:
            return jsonify({
                "error": "No snapshot available and failed to capture new image"
            }), 404
    
    try:
        return send_file(
            snapshot_path,
            mimetype='image/jpeg',
            as_attachment=False,
            download_name='snapshot.jpg'
        )
    except Exception as e:
        logger.error(f"Error serving snapshot: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/video_feed')
def video_feed():
    """
    Video streaming route. Returns Motion JPEG stream.
    
    Returns:
        Response with multipart/x-mixed-replace content type
    """
    logger.info("Video feed request received")
    
    return Response(
        camera.generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/capture')
def capture():
    """
    Trigger a new image capture from the camera.
    
    Returns:
        JSON response with success status
    """
    logger.info("Capture request received")
    
    try:
        success, filepath = capture_snapshot()
        
        if success:
            return jsonify({
                "success": True,
                "message": "Image captured successfully",
                "timestamp": datetime.now().isoformat(),
                "filepath": filepath
            })
        else:
            return jsonify({
                "success": False,
                "error": "Failed to capture image"
            }), 500
            
    except Exception as e:
        logger.error(f"Error in capture endpoint: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/status')
def status():
    """
    Get server and camera status.
    
    Returns:
        JSON response with system status
    """
    return jsonify({
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "camera_index": config.CAMERA_INDEX,
        "images_dir": config.IMAGES_DIR
    })


@app.route('/test_camera')
def test_camera():
    """
    Test camera connectivity.
    
    Returns:
        JSON response with camera test results
    """
    logger.info("Camera test request received")
    
    test_result = camera.test_camera()
    
    return jsonify({
        "success": test_result,
        "message": "Camera test successful" if test_result else "Camera test failed",
        "timestamp": datetime.now().isoformat()
    })


def main():
    """
    Main entry point for the application.
    """
    logger.info("="*60)
    logger.info("Edge IoT Camera Server Starting...")
    logger.info("="*60)
    logger.info(f"Images directory: {config.IMAGES_DIR}")
    logger.info(f"Camera index: {config.CAMERA_INDEX}")
    logger.info(f"Server will listen on: {config.HOST}:{config.PORT}")
    logger.info("="*60)
    
    # Create images directory if it doesn't exist
    os.makedirs(config.IMAGES_DIR, exist_ok=True)
    
    # Test camera before starting server
    logger.info("Testing camera connection...")
    if camera.test_camera():
        logger.info("✓ Camera test successful!")
        
        # Capture initial snapshot
        logger.info("Capturing initial snapshot...")
        success, filepath = capture_snapshot()
        if success:
            logger.info(f"✓ Initial snapshot saved: {filepath}")
        else:
            logger.warning("✗ Failed to capture initial snapshot")
    else:
        logger.warning("✗ Camera test failed! Server will start but camera may not work.")
    
    # Start Flask server
    logger.info("Starting web server...")
    logger.info(f"Access the camera at: http://<your-server-ip>:{config.PORT}/")
    logger.info(f"Direct image URL: http://<your-server-ip>:{config.PORT}/snapshot.jpg")
    
    try:
        app.run(
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG,
            threaded=True
        )
    except KeyboardInterrupt:
        logger.info("\nServer stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")


if __name__ == '__main__':
    main()
