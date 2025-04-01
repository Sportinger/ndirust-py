#!/usr/bin/env python
"""
Test script for the ndirust_py module.
"""

print("Starting test script...")

try:
    import ndirust_py
    print("Successfully imported ndirust_py")
    module_loaded = True
except ImportError as e:
    print(f"Error importing ndirust_py module: {e}")
    print("This might be because the NDI SDK is not installed on your system.")
    print("Please download and install the NDI SDK from https://ndi.tv/tools/")
    module_loaded = False

def main():
    print("Entered main function")
    if not module_loaded:
        print("Module not loaded, exiting")
        return

    print("Testing NDI Python bindings...")
    try:
        version = ndirust_py.get_version_info()
        print(f"Version: {version}")
    except Exception as e:
        print(f"Error getting version: {e}")
    
    # Test basic functionality
    print("\nTesting basic functionality...")
    try:
        if ndirust_py.test_binding():
            print("Basic binding test passed!")
        else:
            print("Basic binding test failed!")
    except Exception as e:
        print(f"Error in test_binding: {e}")
    
    # Print the available submodules
    print("\nAvailable submodules:")
    try:
        for item in dir(ndirust_py):
            if not item.startswith("_") and item not in ["get_version_info", "test_binding"]:
                print(f"- {item}")
    except Exception as e:
        print(f"Error listing submodules: {e}")
    
    print("Test script completed")

if __name__ == "__main__":
    print("Calling main()")
    main()
    print("After main()") 