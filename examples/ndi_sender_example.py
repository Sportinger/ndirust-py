#!/usr/bin/env python
"""
NDI Sender Example

This example shows how to use the ndirust_py module to send NDI video
frames to the network.
"""

import time
import math
import numpy as np
import ndirust_py

def create_test_pattern(width, height, frame_num):
    """Create a simple test pattern as UYVY format (2 bytes per pixel)"""
    # UYVY format: U0 Y0 V0 Y1 (2 pixels = 4 bytes)
    # Each component is 1 byte (0-255)
    buffer_size = width * height * 2  # 2 bytes per pixel in UYVY
    
    # Create a buffer for the UYVY data
    buffer = bytearray(buffer_size)
    
    # Create animated pattern
    t = frame_num * 0.05  # Time variable for animation
    
    # Fill the buffer with a test pattern
    for y in range(height):
        for x in range(0, width, 2):  # Process 2 pixels at a time for UYVY
            # Calculate pattern values
            cx = x / width - 0.5
            cy = y / height - 0.5
            
            # Create some patterns
            circle = 0.5 + 0.5 * math.sin(math.sqrt(cx*cx + cy*cy) * 20 - t * 2)
            waves = 0.5 + 0.5 * math.sin(10 * cx + t) * math.sin(10 * cy + t)
            
            # First pixel's Y (luma)
            y0 = int(255 * waves)
            
            # Second pixel's Y (luma)
            y1 = int(255 * circle)
            
            # Shared U/V (chroma)
            # Create rainbowish effect with time
            u = int(128 + 127 * math.sin(cx * 6.28 + t))
            v = int(128 + 127 * math.sin(cy * 6.28 + t * 1.5))
            
            # Calculate buffer position
            pos = (y * width + x) * 2
            
            # Write UYVY values
            buffer[pos] = u      # U
            buffer[pos+1] = y0    # Y0
            buffer[pos+2] = v     # V
            buffer[pos+3] = y1    # Y1
    
    return bytes(buffer)

def main():
    print("NDI Sender Example")
    print(f"Version: {ndirust_py.get_version_info()}")
    
    # Check if NDI is supported on this CPU
    print("\nChecking NDI SDK availability...")
    if not ndirust_py.is_supported_cpu():
        print("Your CPU does not support NDI")
        return
    
    # Initialize NDI
    print("Initializing NDI...")
    if not ndirust_py.initialize_ndi():
        print("Failed to initialize NDI SDK. Make sure the NDI SDK is installed.")
        return
    
    # Create an NDI sender
    print("\nCreating NDI sender...")
    try:
        # Create a sender with a name that will appear in NDI receivers
        sender = ndirust_py.sender.NdiSender("Python Test Pattern")
        print(f"Created NDI sender: {sender.get_name()}")
        
        # Video parameters
        width = 640
        height = 360
        frame_rate_n = 30
        frame_rate_d = 1  # 30 fps
        
        # Send video frames in a loop
        print("\nSending test pattern frames (Ctrl+C to stop)...")
        frame_num = 0
        
        try:
            while True:
                # Create a test pattern frame
                frame_data = create_test_pattern(width, height, frame_num)
                
                # Send the frame
                sender.send_video(
                    data=frame_data,
                    width=width,
                    height=height,
                    frame_rate_n=frame_rate_n,
                    frame_rate_d=frame_rate_d,
                    fourcc="UYVY"
                )
                
                # Increment frame counter and sleep to achieve the desired frame rate
                frame_num += 1
                time.sleep(1 / (frame_rate_n / frame_rate_d))
                
                # Print progress every 30 frames
                if frame_num % 30 == 0:
                    print(f"Sent {frame_num} frames")
        
        except KeyboardInterrupt:
            print("\nStopped by user")
        
        # Clean up
        sender.close()
        print("Sender closed")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 