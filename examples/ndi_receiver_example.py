#!/usr/bin/env python
"""
NDI Receiver Example

This example shows how to use the ndirust_py module to receive NDI video
frames from the network.
"""

import time
import ndirust_py
from ndirust_py.receiver import FrameType

def main():
    print("NDI Receiver Example")
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
    
    # First, find available sources
    print("\nSearching for NDI sources...")
    try:
        finder = ndirust_py.discovery.NdiFinder()
        sources = finder.find_sources(timeout_ms=2000)  # 2 second timeout
        
        if not sources:
            print("No NDI sources found. Please make sure NDI sources are running.")
            finder.close()
            return
        
        print(f"Found {len(sources)} NDI sources:")
        for idx, source in enumerate(sources):
            print(f"  {idx+1}. {source}")
        
        # Select first source
        selected_source = sources[0]
        print(f"\nConnecting to first source: {selected_source}")
        
        # Create receiver and connect to selected source
        receiver = ndirust_py.receiver.NdiReceiver()
        receiver.connect_to_source(selected_source.name)
        print(f"Connected to NDI source: {selected_source.name}")
        
        # Receive frames for a period of time
        print("\nReceiving frames (10 seconds)...")
        start_time = time.time()
        frame_count = {
            "video": 0,
            "audio": 0,
            "metadata": 0,
            "error": 0,
            "none": 0,
        }
        
        while time.time() - start_time < 10:
            # Receive a frame with a timeout
            frame_type, frame_data = receiver.receive_frame(timeout_ms=500)
            
            if frame_type == FrameType.Video:
                frame_count["video"] += 1
                print(f"Received video frame: {frame_data.width}x{frame_data.height} at timecode {frame_data.timecode}")
                
            elif frame_type == FrameType.Audio:
                frame_count["audio"] += 1
                print(f"Received audio frame: {frame_data.num_channels} channels, {frame_data.num_samples} samples at {frame_data.sample_rate}Hz")
                
            elif frame_type == FrameType.Metadata:
                frame_count["metadata"] += 1
                print(f"Received metadata: {frame_data.data[:40]}...")
                
            elif frame_type == FrameType.Error:
                frame_count["error"] += 1
                print("Error receiving frame")
                
            elif frame_type == FrameType.None:
                frame_count["none"] += 1
                print("No frame received in timeout period")
            
            # Small sleep to prevent high CPU usage
            time.sleep(0.01)
        
        # Print summary
        print("\nReceive summary:")
        for frame_type, count in frame_count.items():
            print(f"  {frame_type.capitalize()}: {count}")
        
        # Clean up
        receiver.close()
        finder.close()
        print("\nReceiver and finder closed")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 