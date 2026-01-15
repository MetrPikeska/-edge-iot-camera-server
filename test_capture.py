#!/usr/bin/env python3
"""
Simple test script to verify camera functionality.
Run this before starting the web server.
"""
import sys
from camera import CameraCapture

def main():
    print("="*60)
    print("Camera Test Script")
    print("="*60)
    
    camera = CameraCapture()
    
    # Test 1: Camera connectivity
    print("\n[Test 1] Testing camera connectivity...")
    if not camera.test_camera():
        print("✗ FAILED: Camera is not accessible")
        print("\nTroubleshooting steps:")
        print("1. Check if camera is connected: ls -l /dev/video0")
        print("2. Check permissions: sudo usermod -a -G video $USER")
        print("3. Restart and try again")
        sys.exit(1)
    
    print("✓ PASSED: Camera is accessible")
    
    # Test 2: Image capture
    print("\n[Test 2] Testing image capture...")
    success, filepath = camera.capture_image(save_with_timestamp=True)
    
    if not success:
        print("✗ FAILED: Could not capture image")
        sys.exit(1)
    
    print(f"✓ PASSED: Image captured successfully")
    print(f"  Saved to: {filepath}")
    
    # Summary
    print("\n" + "="*60)
    print("All tests passed! ✓")
    print("You can now start the web server with: python3 app.py")
    print("="*60)

if __name__ == "__main__":
    main()
