#!/usr/bin/env python
"""
Test script for the NDI sender functionality.
"""

import os
import sys
import time
import ctypes
from ctypes import cdll

print("Starting NDI sender test script...")

# Ensure the NDI SDK is in the PATH for the DLL to be found
ndi_sdk_path = r"C:\Program Files\NDI\NDI 6 SDK\Bin\x64"
os.environ["PATH"] = ndi_sdk_path + os.pathsep + os.environ["PATH"]

# Try to load the NDI DLL directly
print("Loading NDI DLL...")
ndi_dll_path = os.path.join(ndi_sdk_path, "Processing.NDI.Lib.x64.dll")
print(f"Attempting to load: {ndi_dll_path}")

if os.path.exists(ndi_dll_path):
    try:
        ndi_lib = cdll.LoadLibrary(ndi_dll_path)
        print("Successfully loaded NDI DLL!")
    except Exception as e:
        print(f"Failed to load NDI DLL using ctypes: {e}")
        sys.exit(1)
else:
    print(f"The DLL file does not exist at the specified path: {ndi_dll_path}")
    sys.exit(1)

try:
    import ndirust_py
    print("Successfully imported ndirust_py")
except ImportError as e:
    print(f"Error importing ndirust_py module: {e}")
    print("This might be because the NDI SDK is not installed on your system.")
    print("Please download and install the NDI SDK from https://ndi.tv/tools/")
    sys.exit(1)

def main():
    print("Testing NDI Sender...")
    
    try:
        # Check if NDI is supported on this system
        if not ndirust_py.is_supported_cpu():
            print("NDI is not supported on this CPU")
            return
        
        # Initialize NDI
        if not ndirust_py.initialize_ndi():
            print("Failed to initialize NDI")
            return
        
        print("NDI initialized successfully")
        
        # Create an NDI sender
        sender_name = "Python Test Sender"
        sender = ndirust_py.sender.NdiSender(sender_name)
        print(f"Created NDI sender: {sender_name}")
        
        # Send a test pattern
        print("Sending test pattern...")
        for i in range(100):  # Send 100 frames
            sender.send_test_pattern(width=1280, height=720, fps_n=30, fps_d=1)
            time.sleep(1/30)  # Sleep for approximately one frame duration
            if i % 30 == 0:  # Print status every second
                print(f"Sent {i} frames")
        
        print("Test pattern sent!")
        
        # Close the sender
        sender.close()
        print("Sender closed.")
        
    except Exception as e:
        print(f"Error in NDI sender test: {e}")

if __name__ == "__main__":
    main() 