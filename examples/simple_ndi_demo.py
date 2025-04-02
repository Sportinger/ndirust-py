#!/usr/bin/env python
"""
Simple NDI Demo

This example shows how to discover NDI sources and send a test pattern.
"""

import os
import time
import argparse

# Optional fallback path for finding NDI SDK
NDI_SDK_PATH = r"C:\Program Files\NDI\NDI 6 SDK\Bin\x64"
if os.path.exists(NDI_SDK_PATH):
    os.environ["PATH"] = NDI_SDK_PATH + os.pathsep + os.environ.get("PATH", "")

try:
    import ndirust_py
except ImportError:
    print("Could not import ndirust_py. Make sure it's installed!")
    print("Install with: pip install ndirust-py")
    exit(1)

def discover_sources():
    """Discover and print all NDI sources on the network."""
    print("\n--- NDI Source Discovery ---")
    
    # Initialize NDI
    if not ndirust_py.initialize_ndi():
        print("Failed to initialize NDI")
        return False
    
    # Create a finder
    finder = ndirust_py.discovery.NdiFinder()
    print("Searching for NDI sources...")
    
    # Look for sources with a 2 second timeout
    sources = finder.find_sources(timeout_ms=2000)
    
    if sources:
        print(f"Found {len(sources)} NDI sources:")
        for i, source in enumerate(sources, 1):
            print(f"  {i}. {source}")
    else:
        print("No NDI sources found.")
    
    # Clean up
    finder.close()
    return True

def send_test_pattern(duration=5):
    """Send a test pattern for the specified duration."""
    print("\n--- NDI Test Pattern Sender ---")
    
    # Initialize NDI
    if not ndirust_py.initialize_ndi():
        print("Failed to initialize NDI")
        return False
    
    # Create a sender
    sender_name = "Python NDI Demo"
    sender = ndirust_py.sender.NdiSender(sender_name)
    print(f"Created NDI source: {sender_name}")
    
    # Frame parameters
    width = 1280
    height = 720
    fps = 30
    
    # Calculate total frames
    total_frames = duration * fps
    print(f"Sending {total_frames} frames ({duration} seconds) at {fps}fps...")
    
    # Send frames
    start_time = time.time()
    for i in range(total_frames):
        # Send a frame
        sender.send_test_pattern(width=width, height=height, fps_n=fps, fps_d=1)
        
        # Print progress every second
        if i % fps == 0:
            print(f"  Sent {i} frames - {i//fps}s of {duration}s")
        
        # Sleep to maintain correct frame rate
        next_frame_time = start_time + ((i + 1) / fps)
        sleep_time = max(0, next_frame_time - time.time())
        if sleep_time > 0:
            time.sleep(sleep_time)
    
    # Clean up
    sender.close()
    print(f"Sent {total_frames} frames in {time.time() - start_time:.2f} seconds")
    return True

def main():
    parser = argparse.ArgumentParser(description="Simple NDI Demo")
    parser.add_argument("--discover", action="store_true", help="Discover NDI sources")
    parser.add_argument("--send", action="store_true", help="Send test pattern")
    parser.add_argument("--duration", type=int, default=5, help="Duration to send test pattern (seconds)")
    
    args = parser.parse_args()
    
    # Print version info
    print(f"ndirust_py version: {ndirust_py.get_version_info()}")
    print(f"CPU supports NDI: {ndirust_py.is_supported_cpu()}")
    
    # Run requested operations
    if args.discover:
        discover_sources()
    
    if args.send:
        send_test_pattern(args.duration)
    
    # If no options specified, run both
    if not (args.discover or args.send):
        discover_sources()
        send_test_pattern(args.duration)

if __name__ == "__main__":
    main() 