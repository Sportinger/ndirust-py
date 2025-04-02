#!/usr/bin/env python
"""
Test script to demonstrate the NDI package with bundled DLLs.

This script shows how the NDI Python bindings work without requiring a separate
NDI SDK installation, using the included DLLs.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

print("Testing NDI bindings with bundled DLLs")

# First extract the DLL from the wheel to a temporary location
wheel_path = "dist/ndirust_py-0.1.0-cp310-cp310-win_amd64.whl"

if not os.path.exists(wheel_path):
    print(f"Wheel not found at {wheel_path}")
    sys.exit(1)

# Create a temporary directory
temp_dir = Path(tempfile.mkdtemp(prefix="ndirust_py_test_"))
print(f"Created temporary directory: {temp_dir}")

# Extract wheel contents
import zipfile
with zipfile.ZipFile(wheel_path, 'r') as zip_ref:
    # List contents
    content_list = zip_ref.namelist()
    print("Wheel contents:")
    for item in content_list:
        print(f"  {item}")
    
    # Find the DLL path
    dll_path_in_zip = "ndirust_py/bin/win64/Processing.NDI.Lib.x64.dll"
    if dll_path_in_zip not in content_list:
        print(f"DLL not found in wheel at path {dll_path_in_zip}")
        sys.exit(1)
    
    # Extract the DLL
    zip_ref.extract(dll_path_in_zip, temp_dir)
    
    # Extract the Python module
    pyd_file = None
    for file in content_list:
        if file.endswith('.pyd'):
            zip_ref.extract(file, temp_dir)
            pyd_file = file
            
    # Extract Python wrapper modules
    for file in content_list:
        if file.endswith('.py'):
            zip_ref.extract(file, temp_dir)

# Get the path to the extracted DLL
extracted_dll_path = temp_dir / dll_path_in_zip
print(f"Extracted NDI DLL to: {extracted_dll_path}")

# Add the directory containing the DLL to the PATH
os.environ["PATH"] = os.path.dirname(extracted_dll_path) + os.pathsep + os.environ.get("PATH", "")

# Now try to load the module directly from the extracted files
if pyd_file:
    extracted_module_path = temp_dir / pyd_file
    print(f"Extracted Python module to: {extracted_module_path}")
else:
    print("No Python module (.pyd) found in the wheel")
    sys.exit(1)

# Add the directory containing the module to sys.path
sys.path.insert(0, str(temp_dir))

try:
    # Import the module
    import ndirust_py
    print("Successfully imported ndirust_py module!")
    
    # Test NDI functionality
    print(f"NDI Version: {ndirust_py.get_version_info()}")
    print(f"CPU Supports NDI: {ndirust_py.is_supported_cpu()}")
    
    # Initialize NDI
    if ndirust_py.initialize_ndi():
        print("Successfully initialized NDI")
        
        # Test source discovery
        print("Looking for NDI sources...")
        finder = ndirust_py.discovery.NdiFinder()
        sources = finder.find_sources(timeout_ms=2000)
        
        if sources:
            print(f"Found {len(sources)} NDI sources:")
            for i, source in enumerate(sources, 1):
                print(f"  {i}. {source}")
        else:
            print("No NDI sources found.")
        
        finder.close()
    else:
        print("Failed to initialize NDI")
    
except ImportError as e:
    print(f"Error importing ndirust_py: {e}")
except Exception as e:
    print(f"Error: {e}")

# Clean up
print("Cleaning up...")
try:
    shutil.rmtree(temp_dir)
    print(f"Removed temporary directory: {temp_dir}")
except Exception as e:
    print(f"Error removing temporary directory: {e}")

print("Test completed") 