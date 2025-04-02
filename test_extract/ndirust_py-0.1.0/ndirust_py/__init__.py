"""
NDI Python bindings using Rust.

This package provides Python bindings for NewTek's NDI technology.
"""

import os
import sys
import platform
import ctypes
import tempfile
import shutil
from ctypes import cdll
from pathlib import Path
import logging
import pkg_resources

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ndirust_py")

# Create a global variable to keep track of temporary directories
_temp_dirs = []

def _find_bundled_ndi_lib():
    """Extract and find the bundled NDI library."""
    system = platform.system()
    
    if system == "Windows":
        resource_path = "bin/win64/Processing.NDI.Lib.x64.dll"
        lib_name = "Processing.NDI.Lib.x64.dll"
    elif system == "Darwin":  # macOS
        resource_path = "bin/macos/libndi.4.dylib"
        lib_name = "libndi.4.dylib"
    else:  # Linux
        resource_path = "bin/linux/libndi.so.4"
        lib_name = "libndi.so.4"
    
    # Check if the resource exists in the package
    try:
        if pkg_resources.resource_exists("ndirust_py", resource_path):
            # Create a temporary directory
            temp_dir = tempfile.mkdtemp(prefix="ndirust_py_")
            _temp_dirs.append(temp_dir)  # Store for cleanup later
            
            # Extract the library to the temporary directory
            lib_data = pkg_resources.resource_string("ndirust_py", resource_path)
            lib_path = os.path.join(temp_dir, lib_name)
            
            # Write the library data to the temporary file
            with open(lib_path, "wb") as f:
                f.write(lib_data)
            
            logger.debug(f"Extracted NDI library to: {lib_path}")
            return os.path.dirname(lib_path)
    except Exception as e:
        logger.warning(f"Failed to extract bundled NDI library: {e}")
    
    return None

def _find_system_ndi_sdk():
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
    # First try to use our bundled library
    ndi_sdk_path = _find_bundled_ndi_lib()
    
    # If that fails, try to find it on the system
    if not ndi_sdk_path:
        ndi_sdk_path = _find_system_ndi_sdk()
    
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

# Clean up temporary directories when the module is unloaded
def _cleanup_temp_dirs():
    """Remove temporary directories created for NDI libraries."""
    for temp_dir in _temp_dirs:
        try:
            shutil.rmtree(temp_dir)
        except:
            pass

# Register cleanup function
import atexit
atexit.register(_cleanup_temp_dirs)

# Load NDI library before importing the Rust module
_load_ndi_library()

try:
    # Import the actual Rust module
    from .ndirust_py import *
    from .ndirust_py import discovery, sender, receiver
except ImportError as e:
    logger.error(f"Error importing ndirust_py module: {e}")
    logger.error("Make sure the NDI SDK is installed or this package has bundled DLLs")
    raise ImportError("Failed to import ndirust_py module") from e

# Set version
__version__ = get_version_info().split()[-1]

def __getattr__(name):
    if name == "version":
        return __version__
    raise AttributeError(f"module 'ndirust_py' has no attribute '{name}'") 