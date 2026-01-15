"""
Camera module for capturing images from USB camera using OpenCV.
Designed for headless Ubuntu Server with USB camera on /dev/video0.
"""
import cv2
import os
import logging
from datetime import datetime
from typing import Optional, Tuple, Generator
import threading
import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global lock for camera access (only one thread can use camera at a time)
camera_lock = threading.Lock()


class CameraCapture:
    """
    Handles USB camera operations for capturing images.
    Uses OpenCV (cv2) with headless backend suitable for Ubuntu Server.
    """
    
    def __init__(self, camera_index: int = config.CAMERA_INDEX):
        """
        Initialize camera capture.
        
        Args:
            camera_index: Camera device index (0 for /dev/video0)
        """
        self.camera_index = camera_index
        self.camera = None
        
        # Ensure images directory exists
        os.makedirs(config.IMAGES_DIR, exist_ok=True)
        logger.info(f"Images directory: {config.IMAGES_DIR}")
    
    def _open_camera(self) -> bool:
        """
        Open camera connection with proper settings for headless operation.
        
        Returns:
            True if camera opened successfully, False otherwise
        """
        try:
            # Use V4L2 backend for Linux USB cameras
            self.camera = cv2.VideoCapture(
                self.camera_index,
                cv2.CAP_V4L2
            )
            
            if not self.camera.isOpened():
                logger.error(f"Failed to open camera at index {self.camera_index}")
                return False
            
            # Set camera properties
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
            self.camera.set(cv2.CAP_PROP_FPS, config.CAMERA_FPS)
            
            # Try to enable auto exposure and auto white balance
            self.camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)  # Auto exposure
            self.camera.set(cv2.CAP_PROP_AUTOFOCUS, 1)  # Auto focus if available
            
            # Log actual camera settings
            actual_width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
            actual_height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
            actual_fps = self.camera.get(cv2.CAP_PROP_FPS)
            
            logger.info(f"Camera opened: {actual_width}x{actual_height} @ {actual_fps}fps")
            return True
            
        except Exception as e:
            logger.error(f"Error opening camera: {e}")
            return False
    
    def _close_camera(self):
        """Release camera resources."""
        if self.camera is not None:
            self.camera.release()
            self.camera = None
            logger.info("Camera released")
    
    def capture_image(self, save_with_timestamp: bool = True) -> Tuple[bool, Optional[str]]:
        """
        Capture a single frame from the camera and save it to disk.
        Thread-safe: uses lock to prevent concurrent camera access.
        
        Args:
            save_with_timestamp: If True, saves both timestamped and latest versions
        
        Returns:
            Tuple of (success: bool, filepath: Optional[str])
        """
        # Acquire lock to ensure exclusive camera access
        with camera_lock:
            logger.debug("Camera lock acquired for capture")
            
            # Open camera
            if not self._open_camera():
                return False, None
        
        try:
            # Allow camera to warm up (important for USB cameras)
            # Some cameras need more warm-up time
            logger.info("Warming up camera...")
            for i in range(10):
                ret, _ = self.camera.read()
                if i % 3 == 0:
                    logger.debug(f"Warmup frame {i+1}/10")
            
            # Small delay for camera stabilization
            import time
            time.sleep(0.5)
            
            # Capture frame
            ret, frame = self.camera.read()
            
            if not ret or frame is None:
                logger.error("Failed to capture frame from camera")
                return False, None
            
            logger.info(f"Frame captured: {frame.shape}")
            
            # Save latest snapshot (always overwrite)
            latest_path = os.path.join(config.IMAGES_DIR, config.LATEST_IMAGE_NAME)
            cv2.imwrite(latest_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
            logger.info(f"Latest snapshot saved: {latest_path}")
            
            # Save timestamped version if requested
            if save_with_timestamp:
                timestamp = datetime.now().strftime(config.TIMESTAMP_FORMAT)
                timestamped_filename = f"snapshot_{timestamp}.jpg"
                timestamped_path = os.path.join(config.IMAGES_DIR, timestamped_filename)
            except Exception as e:
                logger.error(f"Error during image capture: {e}")
                return False, None
                
            finally:
                # Always release camera
                self._close_camera()
                logger.debug("Camera lock released"r during image capture: {e}")
            return False, None
            
        finally:
            # Always release camera
            self._close_camera()
    
    def test_camera(self) -> bool:
        """
        Thread-safe: uses lock to prevent concurrent camera access.
        
        Returns:
            True if camera test successful, False otherwise
        """
        with camera_lock:
            logger.info("Testing camera connection...")
            
            if not self._open_camera():
                return False
            
            try:
                ret, frame = self.camera.read()
                success = ret and frame is not None
                
                if success:
                    logger.info("✓ Camera test successful")
                else:
                    logger.error("✗ Camera test failed - unable to read frame")
                
                return success
                
            except Exception as e:
                logger.error(f"✗ Camera test failed: {e}")
                return False
                
            finally:
            finally:
            self._close_camera()
    
    def generate_frames(self) -> Generator[bytes, None, None]:
        Thread-safe: uses lock for each frame to allow capture during streaming.
        
        Yields:
            JPEG encoded frame bytes
        """
        logger.info("Starting video stream...")
        frame_count = 0
        
        try:
            while True:
                # Acquire lock for each frame (allows other operations between frames)
                with camera_lock:
                    # Open camera if not open
                    if self.camera is None or not self.camera.isOpened():
                        if not self._open_camera():
                            logger.error("Failed to open camera for streaming")
                            break
                        # Warmup only on first open
                        if frame_count == 0:
                            for _ in range(5):
                                self.camera.read()
                    
                    # Read frame
                    ret, frame = self.camera.read()
                    
                    if not ret or frame is None:
                        logger.warning("Failed to read frame from camera")
                        self._close_camera()
                        continue
                    
                    # Encode frame as JPEG
                    ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                    
                    if not ret:
                        logger.warning("Failed to encode frame")
                        continue
                    
                    frame_bytes = buffer.tobytes()
                
                # Yield frame outside of lock (allows other threads to access camera)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                
                frame_count += 1
                if frame_count % 100 == 0:
                    logger.debug(f"Streamed {frame_count} frames")
                    
        except GeneratorExit:
            logger.info("Video stream stopped by client")
        except Exception as e:
            logger.error(f"Error during video streaming: {e}")
        finally:
            with camera_lock:
            except Exception as e:
            logger.error(f"Error during video streaming: {e}")
        finally:
            self._close_camera()
            logger.info(f"Video stream ended. Total frames: {frame_count}")


def capture_snapshot() -> Tuple[bool, Optional[str]]:
    """
    Convenience function to capture a snapshot.
    
    Returns:
        Tuple of (success: bool, filepath: Optional[str])
    """
    camera = CameraCapture()
    return camera.capture_image(save_with_timestamp=True)


if __name__ == "__main__":
    # Test camera when run directly
    print("Testing camera connection...")
    camera = CameraCapture()
    
    if camera.test_camera():
        print("\nCapturing test snapshot...")
        success, filepath = camera.capture_image(save_with_timestamp=True)
        
        if success:
            print(f"✓ Success! Image saved to: {filepath}")
        else:
            print("✗ Failed to capture image")
    else:
        print("✗ Camera test failed")
