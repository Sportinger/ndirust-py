#!/usr/bin/env python
"""
Simplified test script for the NDI receiver functionality.
"""

import os
import sys
import time

# Ensure the NDI SDK is in the PATH
ndi_sdk_path = r"C:\Program Files\NDI\NDI 6 SDK\Bin\x64"
os.environ["PATH"] = ndi_sdk_path + os.pathsep + os.environ["PATH"]

try:
    import ndirust_py
    print("Successfully imported ndirust_py")
except ImportError as e:
    print(f"Error importing ndirust_py module: {e}")
    sys.exit(1)

# Frame type values
FRAME_NONE = 0
FRAME_VIDEO = 1
FRAME_AUDIO = 2
FRAME_METADATA = 3
FRAME_ERROR = 4

def display_frame_info(frame_type, frame):
    """Display information about a received NDI frame."""
    # Get the name of the frame type
    frame_type_names = ["None", "Video", "Audio", "Metadata", "Error"]
    frame_type_name = frame_type_names[frame_type] if 0 <= frame_type < len(frame_type_names) else f"Unknown ({frame_type})"
    
    print(f"Received frame type: {frame_type_name}")
    
    if frame_type == FRAME_VIDEO and frame is not None:
        print(f"Video Frame: {frame.width}x{frame.height} @ {frame.frame_rate_n}/{frame.frame_rate_d} fps")
        if hasattr(frame, 'get_four_cc_name'):
            print(f"Format: {frame.get_four_cc_name()}")
        print(f"Timecode: {frame.timecode}")
        print(f"Data size: {frame.data_size} bytes")
    
    elif frame_type == FRAME_AUDIO and frame is not None:
        print(f"Audio Frame: {frame.sample_rate} Hz, {frame.num_channels} channels, {frame.num_samples} samples")
        print(f"Timecode: {frame.timecode}")
    
    elif frame_type == FRAME_METADATA and frame is not None:
        print(f"Metadata Frame: {frame.data[:50]}...")
        print(f"Timecode: {frame.timecode}")
        
    elif frame is None:
        print("No frame data received")

def main():
    print("\n=== Testing NDI Receiver ===\n")
    
    try:
        # Initialize NDI
        if not ndirust_py.initialize_ndi():
            print("Failed to initialize NDI")
            return
        
        print("NDI initialized successfully")
        
        # Find available sources
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
        
        print("Successfully connected to source")
        
        # Receive frames for a few seconds
        print("\nReceiving frames for 10 seconds...\n")
        start_time = time.time()
        frame_count = 0
        
        while time.time() - start_time < 10:  # Run for 10 seconds
            # Receive a frame with 500ms timeout
            frame_type_obj, frame = receiver.receive_frame(timeout_ms=500)
            
            # Convert the frame_type enum to integer for easier handling
            frame_type = int(frame_type_obj)
            
            # Display frame information for non-empty frames
            if frame_type != FRAME_NONE:
                display_frame_info(frame_type, frame)
                frame_count += 1
                print("-" * 40)
            
            # Brief pause to avoid flooding the console
            time.sleep(0.01)
        
        # Print summary
        print(f"\nReceived {frame_count} frames in {time.time() - start_time:.2f} seconds")
        
        # Clean up
        receiver.close()
        finder.close()
        print("Receiver and finder closed")
        
    except Exception as e:
        print(f"Error in NDI receiver test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 