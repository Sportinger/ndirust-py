#!/usr/bin/env python
"""
Build and test script for ndirust-py.

This script automates the build and testing process for the ndirust_py library.
It performs the following steps:
1. Builds the library using maturin
2. Tests basic functionality
"""

import subprocess
import sys
import os
import time
import ctypes
from ctypes import cdll

def run_command(command, cwd=None):
    """Run a shell command and print output."""
    print(f"Running: {command}")
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',  # Use UTF-8 encoding
        errors='replace',  # Replace invalid characters
        cwd=cwd
    )
    
    for line in process.stdout:
        print(line, end='')
    
    process.wait()
    return process.returncode

def build_library():
    """Build the Rust library using maturin."""
    print("\n=== Building Library ===\n")
    result = run_command("maturin develop")
    if result != 0:
        print("Failed to build library")
        sys.exit(1)
    
    return True

def load_ndi_dll():
    """Explicitly load the NDI DLL to ensure it's available."""
    print("\n=== Loading NDI DLL ===\n")
    
    # Try to load the NDI DLL directly
    ndi_sdk_path = r"C:\Program Files\NDI\NDI 6 SDK\Bin\x64"
    
    # Add the SDK path to the system PATH
    os.environ["PATH"] = ndi_sdk_path + os.pathsep + os.environ["PATH"]
    
    # Try to load Processing.NDI.Lib.x64.dll
    ndi_dll_path = os.path.join(ndi_sdk_path, "Processing.NDI.Lib.x64.dll")
    print(f"Attempting to load: {ndi_dll_path}")
    
    if os.path.exists(ndi_dll_path):
        # Try to load the NDI library using ctypes
        try:
            ndi_lib = cdll.LoadLibrary(ndi_dll_path)
            print("Successfully loaded NDI DLL!")
            return True
        except Exception as e:
            print(f"Failed to load NDI DLL using ctypes: {e}")
            return False
    else:
        print(f"The DLL file does not exist at the specified path: {ndi_dll_path}")
        return False

def test_ndi_finder():
    """Test NDI source discovery."""
    print("\n=== Testing NDI Source Discovery ===\n")
    
    try:
        # Try to import and use the library
        import ndirust_py
        
        print(f"Library version: {ndirust_py.get_version_info()}")
        print(f"CPU supports NDI: {ndirust_py.is_supported_cpu()}")
        
        # Initialize NDI
        ndirust_py.initialize_ndi()
        print("NDI initialized successfully")
        
        # Test source finder
        finder = ndirust_py.discovery.NdiFinder()
        print("Created NDI finder")
        
        # Look for sources
        print("Searching for NDI sources...")
        sources = finder.find_sources(timeout_ms=1000)
        
        if sources:
            print(f"Found {len(sources)} sources:")
            for i, source in enumerate(sources, 1):
                print(f"  {i}. {source}")
        else:
            print("No NDI sources found.")
        
        # Clean up
        finder.close()
        print("Finder closed.")
        return True
    
    except Exception as e:
        print(f"Error testing NDI finder: {e}")
        return False

def main():
    """Main function."""
    # Build the library
    if not build_library():
        return
    
    # Load the NDI DLL explicitly
    if not load_ndi_dll():
        print("Failed to load NDI DLL. Make sure the NDI SDK is installed correctly.")
        return
    
    # Test basic functionality
    if not test_ndi_finder():
        return
    
    print("\n=== All tests completed successfully ===")

if __name__ == "__main__":
    main() 