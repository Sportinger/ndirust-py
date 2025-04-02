"""
NDI Python bindings using Rust.

This package provides Python bindings for NewTek's NDI technology.
"""

import os
import sys
import platform
import ctypes
from ctypes import cdll
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ndirust_py")

# Try to find and load NDI DLL
def _find_ndi_sdk():
    """Find the NDI SDK path on the system."""
    system = platform.system()
    
    if system == "Windows":
        # Common NDI SDK install locations on Windows
        possible_locations = [
            r"C:\Program Files\NDI\NDI 6 SDK\Bin\x64",
            r"C:\Program Files\NDI\NDI 5 SDK\Bin\x64",
            r"C:\Program Files\NDI\NDI 4 SDK\Bin\x64",
            r"C:\Program Files\NDI\NDI Runtime\v5",
            r"C:\Program Files\NDI\NDI Runtime\v4"
        ]
        
        dll_name = "Processing.NDI.Lib.x64.dll"
    elif system == "Darwin":  # macOS
        possible_locations = [
            "/usr/local/lib",
            "/Library/NDI SDK for Apple/lib",
            "/Applications/NDI SDK for Apple/lib"
        ]
        
        dll_name = "libndi.4.dylib"
    else:  # Linux
        possible_locations = [
            "/usr/lib",
            "/usr/local/lib",
            "/opt/ndi/lib"
        ]
        
        dll_name = "libndi.so.4"
    
    # Check environment variable
    ndi_runtime = os.environ.get("NDI_RUNTIME_DIR_V4")
    if ndi_runtime:
        possible_locations.insert(0, ndi_runtime)
    
    # Check each location
    for location in possible_locations:
        path = Path(location) / dll_name
        if path.exists():
            return str(path.parent)
    
    return None

def _load_ndi_library():
    """Load the NDI library."""
    ndi_sdk_path = _find_ndi_sdk()
    
    if ndi_sdk_path:
        logger.debug(f"Found NDI SDK at: {ndi_sdk_path}")
        
        # Add to PATH environment variable
        path_sep = os.pathsep
        if ndi_sdk_path not in os.environ.get("PATH", ""):
            os.environ["PATH"] = ndi_sdk_path + path_sep + os.environ.get("PATH", "")
        
        system = platform.system()
        if system == "Windows":
            dll_path = os.path.join(ndi_sdk_path, "Processing.NDI.Lib.x64.dll")
        elif system == "Darwin":  # macOS
            dll_path = os.path.join(ndi_sdk_path, "libndi.4.dylib")
        else:  # Linux
            dll_path = os.path.join(ndi_sdk_path, "libndi.so.4")
        
        try:
            ndi_lib = cdll.LoadLibrary(dll_path)
            logger.debug("Successfully loaded NDI library")
            return True
        except Exception as e:
            logger.warning(f"Failed to load NDI library: {e}")
            return False
    else:
        logger.warning("Could not find NDI SDK. Please install NDI SDK from https://ndi.tv/tools/")
        return False

# Load NDI library before importing the Rust module
_load_ndi_library()

try:
    # Import the actual Rust module
    from .ndirust_py import *
    from .ndirust_py import discovery, sender, receiver
except ImportError as e:
    logger.error(f"Error importing ndirust_py module: {e}")
    logger.error("Make sure the NDI SDK is installed and its DLL/shared library is in PATH")
    raise ImportError("Failed to import ndirust_py module") from e

# Set version
__version__ = get_version_info().split()[-1]

def __getattr__(name):
    if name == "version":
        return __version__
    raise AttributeError(f"module 'ndirust_py' has no attribute '{name}'") 