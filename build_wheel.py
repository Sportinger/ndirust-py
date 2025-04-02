#!/usr/bin/env python
"""
Build wheel package for distribution.
This script will build the wheel package for ndirust-py.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and print output."""
    print(f"Running: {cmd}")
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',
        errors='replace',
        cwd=cwd
    )
    
    for line in process.stdout:
        print(line, end='')
    
    process.wait()
    return process.returncode

def main():
    # Directory setup
    current_dir = Path.cwd()
    dist_dir = current_dir / "dist"
    wheels_dir = current_dir / "target" / "wheels"
    
    # Clean previous builds
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir(exist_ok=True)
    
    # Build the wheel
    print("Building wheel package...")
    result = run_command("maturin build --release")
    if result != 0:
        print("Failed to build wheel package")
        sys.exit(1)
    
    # Copy wheel to dist directory
    if wheels_dir.exists():
        for wheel in wheels_dir.glob("*.whl"):
            dest = dist_dir / wheel.name
            shutil.copy(wheel, dest)
            print(f"Copied {wheel.name} to {dest}")
    
    print("\nWheel build completed! Files are in the 'dist' directory.")
    print("To install the wheel, run:")
    print(f"pip install {dist_dir}/ndirust_py-0.1.0-*.whl")
    
    print("\nTo upload to PyPI, run:")
    print("python -m twine upload dist/*.whl")

if __name__ == "__main__":
    main() 