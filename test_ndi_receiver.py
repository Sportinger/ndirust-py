#!/usr/bin/env python
"""
Test script for the NDI receiver functionality.
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

# Print the available FrameType enum values
print("\nAvailable FrameType values:")
for attr in dir(ndirust_py.receiver.FrameType):
    if not attr.startswith('_'):
        value = getattr(ndirust_py.receiver.FrameType, attr)
        print(f"  {attr}: {value}")

def display_frame_info(frame_type, frame):
    """Display information about a received NDI frame."""
    # Get the name of the frame type
    if frame_type == ndirust_py.receiver.FrameType.Video:
        frame_type_name = "Video"
    elif frame_type == ndirust_py.receiver.FrameType.Audio:
        frame_type_name = "Audio"
    elif frame_type == ndirust_py.receiver.FrameType.Metadata:
        frame_type_name = "Metadata"
    elif frame_type == ndirust_py.receiver.FrameType.Error:
        frame_type_name = "Error"
    elif frame_type == ndirust_py.receiver.FrameType.None:
        frame_type_name = "None"
    else:
        frame_type_name = f"Unknown ({frame_type})"
    
    print(f"\nReceived frame type: {frame_type_name}")
    
    if frame_type == ndirust_py.receiver.FrameType.Video and frame is not None:
        print(f"Video Frame: {frame.width}x{frame.height} @ {frame.frame_rate_n}/{frame.frame_rate_d} fps")
        print(f"Format: {frame.get_four_cc_name()}")
        print(f"Timecode: {frame.timecode}")
        print(f"Data size: {frame.data_size} bytes")
        if frame.data:
            print("Frame contains image data")
        else:
            print("Frame does not contain image data")
    
    elif frame_type == ndirust_py.receiver.FrameType.Audio and frame is not None:
        print(f"Audio Frame: {frame.sample_rate} Hz, {frame.num_channels} channels")
        print(f"Samples: {frame.num_samples}")
        print(f"Timecode: {frame.timecode}")
        print(f"Data size: {frame.data_size} bytes")
    
    elif frame_type == ndirust_py.receiver.FrameType.Metadata and frame is not None:
        print(f"Metadata Frame:")
        print(f"Timecode: {frame.timecode}")
        print(f"Data: {frame.data[:100]}...")
        
    elif frame is None:
        print("No frame data received")

def main():
    print("\n=== Testing NDI Receiver ===\n")
    
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
        
        # First, find available sources
        print("Looking for NDI sources...")
        finder = ndirust_py.discovery.NdiFinder()
        sources = finder.find_sources(timeout_ms=3000)
        
        if not sources:
            print("No NDI sources found. Please ensure there's an NDI source running.")
            finder.close()
            return
        
        # Print available sources
        print(f"Found {len(sources)} NDI sources:")
        for i, source in enumerate(sources, 1):
            print(f"  {i}. {source}")
        
        # Create an NDI receiver
        receiver = ndirust_py.receiver.NdiReceiver()
        print("Created NDI receiver")
        
        # Get the name of the first source
        source_name = str(sources[0])
        source_name = source_name.replace("NdiSource(name='", "").replace("')", "")
        
        # Connect to the source
        print(f"Connecting to source: {source_name}")
        receiver.connect_to_source(source_name)
        
        # We don't need to check get_connected_source() as it might not be available
        # Just move forward with the receiver
        print("Successfully connected to source, receiving frames...")
        
        # Receive frames for a few seconds
        print("\nReceiving frames for 10 seconds...\n")
        start_time = time.time()
        frame_count = 0
        
        while time.time() - start_time < 10:  # Run for 10 seconds
            # Receive a frame with 500ms timeout
            frame_type, frame = receiver.receive_frame(timeout_ms=500)
            
            # Display frame information
            if frame_type != ndirust_py.receiver.FrameType.None:
                display_frame_info(frame_type, frame)
                frame_count += 1
            
            # Brief pause
            time.sleep(0.01)
        
        # Print summary
        print(f"\nReceived {frame_count} frames in {time.time() - start_time:.2f} seconds")
        
        # Clean up
        receiver.close()
        finder.close()
        print("Receiver and finder closed.")
        
    except Exception as e:
        print(f"Error in NDI receiver test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 