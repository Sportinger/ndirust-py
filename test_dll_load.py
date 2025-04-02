#!/usr/bin/env python
"""
Test script to explicitly load the NDI DLL before importing our module.
"""

import os
import sys
import ctypes
from ctypes import cdll

def main():
    print("Testing NDI DLL loading")
    
    # Try to load the NDI DLL directly
    ndi_sdk_path = r"C:\Program Files\NDI\NDI 6 SDK\Bin\x64"
    
    # Add the SDK path to the system PATH
    os.environ["PATH"] = ndi_sdk_path + os.pathsep + os.environ["PATH"]
    
    # List all DLLs in the NDI SDK directory
    print(f"Looking for DLLs in: {ndi_sdk_path}")
    dlls = [f for f in os.listdir(ndi_sdk_path) if f.lower().endswith('.dll')]
    print(f"Available DLLs: {dlls}")
    
    try:
        # Try to load Processing.NDI.Lib.x64.dll
        ndi_dll_path = os.path.join(ndi_sdk_path, "Processing.NDI.Lib.x64.dll")
        print(f"Attempting to load: {ndi_dll_path}")
        
        if os.path.exists(ndi_dll_path):
            # Try to load the NDI library using ctypes
            try:
                ndi_lib = cdll.LoadLibrary(ndi_dll_path)
                print("Successfully loaded NDI DLL!")
            except Exception as e:
                print(f"Failed to load NDI DLL using ctypes: {e}")
        else:
            print(f"The DLL file does not exist at the specified path: {ndi_dll_path}")
        
        # Now try importing our module
        print("\nTrying to import ndirust_py module...")
        import ndirust_py
        print("Successfully imported ndirust_py!")
        
        # Try using a function from the module
        version = ndirust_py.get_version_info()
        print(f"NDI Rust Python bindings version: {version}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 