#!/usr/bin/env python
"""
NDI Finder Example

This example shows how to use the ndirust_py module to find NDI sources
on the network.
"""

import time
import ndirust_py

def main():
    print("NDI Finder Example")
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
    
    # Create an NDI finder
    print("\nCreating NDI finder and searching for sources...")
    try:
        finder = ndirust_py.discovery.NdiFinder()
        
        # Search for sources with a timeout
        for i in range(3):
            print(f"\nSearch attempt {i+1}...")
            sources = finder.find_sources(timeout_ms=1000)  # 1 second timeout
            
            if sources:
                print(f"Found {len(sources)} NDI sources:")
                for idx, source in enumerate(sources):
                    print(f"  {idx+1}. {source}")
            else:
                print("No NDI sources found")
            
            time.sleep(1)  # Wait a bit before searching again
        
        # Clean up
        finder.close()
        print("\nFinder closed")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 