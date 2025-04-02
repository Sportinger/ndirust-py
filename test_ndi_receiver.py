#!/usr/bin/env python
"""
Test script to check if we can see the NDI source created by our sender.
"""

import os
import sys
import time
import ctypes
from ctypes import cdll

print("Starting NDI receiver test script...")

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
    print("Testing NDI Source Discovery...")
    
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
        
        # Create an NDI finder to look for sources
        finder = ndirust_py.discovery.NdiFinder()
        print("Created NDI finder")
        
        # Look for sources
        print("Starting source discovery loop...")
        print("This will continuously check for NDI sources.")
        print("The Python Test Sender should appear if it's running.")
        print("Press Ctrl+C to stop...")
        
        try:
            while True:
                sources = finder.find_sources(timeout_ms=1000)
                
                if sources:
                    print(f"\nFound {len(sources)} sources:")
                    for i, source in enumerate(sources, 1):
                        print(f"  {i}. {source}")
                else:
                    print("No NDI sources found.", end="\r")
                
                time.sleep(1)  # Check every second
        except KeyboardInterrupt:
            print("\nUser interrupted. Stopping...")
        
        # Clean up
        finder.close()
        print("Finder closed.")
        
    except Exception as e:
        print(f"Error in NDI source discovery: {e}")

if __name__ == "__main__":
    main() 