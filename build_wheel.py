#!/usr/bin/env python
"""
Build script for ndirust-py

This script:
1. Builds the Rust bindings with Maturin
2. Copies the wheel to the dist directory
3. Provides instructions for installation and publishing
"""

import os
import sys
import glob
import shutil
import subprocess
from pathlib import Path


def check_dependencies():
    """Check if necessary dependencies are installed."""
    try:
        # Check for maturin
        subprocess.run(
            ["maturin", "--version"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            check=True
        )
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Error: maturin is not installed or not found in PATH.")
        print("Please install it with: pip install maturin")
        return False
    
    return True


def build_wheel():
    """Build the wheel package using maturin."""
    print("Building wheel package...")
    
    # Build with maturin in release mode
    try:
        # Use shell=True for Windows compatibility
        if os.name == 'nt':  # Windows
            result = subprocess.run(
                "maturin build --release",
                shell=True,
                check=False
            )
        else:
            result = subprocess.run(
                ["maturin", "build", "--release"],
                check=False
            )
        
        if result.returncode != 0:
            print("Error: Failed to build the wheel package.")
            return False
    except Exception as e:
        print(f"Error executing maturin: {e}")
        return False
    
    # Copy wheel to dist directory
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)
    
    # Find the built wheel
    wheels = list(Path("target/wheels").glob("ndirust_py-*.whl"))
    if not wheels:
        print("Error: No wheel file found after build.")
        return False
    
    # Get the latest wheel (sort by modification time)
    latest_wheel = max(wheels, key=os.path.getmtime)
    
    # Copy the wheel to dist
    dest_path = dist_dir / latest_wheel.name
    shutil.copy2(latest_wheel, dest_path)
    print(f"Copied {latest_wheel} to {dest_path}")
    
    return True


def main():
    """Main function."""
    print("=" * 80)
    print("ndirust-py Build Script")
    print("=" * 80)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Build the wheel
    if not build_wheel():
        sys.exit(1)
    
    # Success
    print("\nWheel build completed! Files are in the 'dist' directory.")
    print("To install the wheel, run:")
    
    # Get path to the wheel in a platform-independent way
    wheel_path = os.path.join(os.path.abspath("dist"), "ndirust_py-0.1.0-*.whl")
    print(f"pip install {wheel_path}")
    
    print("\nTo upload to PyPI, run:")
    print("python -m twine upload dist/*.whl")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main() 