"""
Main entry point for ndirust-py.
Run this module directly with:
    python -m ndirust_py
"""

import sys
import time
import argparse
from . import initialize_ndi, is_supported_cpu, get_version_info


def discover_sources(timeout=2000, count=1):
    """Discover NDI sources on the network."""
    from . import discovery
    
    print(f"Searching for NDI sources (timeout: {timeout}ms)...")
    
    # Create finder
    finder = discovery.NdiFinder()
    
    # Search for sources multiple times if requested
    for i in range(count):
        print(f"Search {i+1}/{count}...", end=" ")
        sources = finder.find_sources(timeout_ms=timeout)
        
        if sources:
            print(f"Found {len(sources)} sources:")
            for idx, source in enumerate(sources, 1):
                print(f"  {idx}. {source}")
        else:
            print("No sources found.")
        
        # Wait between searches
        if i < count - 1:
            time.sleep(1)
    
    # Clean up
    finder.close()


def send_test_pattern(name="Test Sender", width=1280, height=720, fps=30, duration=5):
    """Send a test pattern."""
    from . import sender
    
    print(f"Creating NDI sender '{name}'...")
    ndi_sender = sender.NdiSender(name)
    
    frames = fps * duration
    print(f"Sending {frames} frames of {width}x{height} @ {fps} fps for {duration} seconds...")
    
    for i in range(frames):
        ndi_sender.send_test_pattern(width=width, height=height, fps_n=fps, fps_d=1)
        # Show progress
        if i % fps == 0:
            print(f"Sent {i} frames ({i//fps} seconds)...")
        time.sleep(1/fps)
    
    print(f"Sent {frames} frames.")
    ndi_sender.close()
    print("Sender closed.")


def main():
    """Run the main CLI interface."""
    parser = argparse.ArgumentParser(description="NDI Python Bindings Demo")
    parser.add_argument('--version', action='store_true', help='Show version information')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Discover command
    discover_parser = subparsers.add_parser('discover', help='Discover NDI sources')
    discover_parser.add_argument('--timeout', type=int, default=2000, help='Timeout in milliseconds')
    discover_parser.add_argument('--count', type=int, default=1, help='Number of searches to perform')
    
    # Send command
    send_parser = subparsers.add_parser('send', help='Send a test pattern')
    send_parser.add_argument('--name', type=str, default="Python Test Pattern", help='Name of the NDI source')
    send_parser.add_argument('--width', type=int, default=1280, help='Width of the test pattern')
    send_parser.add_argument('--height', type=int, default=720, help='Height of the test pattern')
    send_parser.add_argument('--fps', type=int, default=30, help='Frames per second')
    send_parser.add_argument('--duration', type=int, default=5, help='Duration in seconds')
    
    args = parser.parse_args()
    
    # Check if NDI is supported
    if not is_supported_cpu():
        print("Error: NDI is not supported on this CPU")
        return 1
    
    # Initialize NDI
    if not initialize_ndi():
        print("Error: Failed to initialize NDI")
        return 1
    
    if args.version:
        version = get_version_info()
        print(f"ndirust-py version: {version}")
        return 0
    
    if args.command == 'discover':
        discover_sources(args.timeout, args.count)
    elif args.command == 'send':
        send_test_pattern(args.name, args.width, args.height, args.fps, args.duration)
    else:
        # Default to discover if no command specified
        print(f"ndirust-py v{get_version_info().split()[-1]}")
        print("Available commands:")
        print("  discover - Find NDI sources on the network")
        print("  send     - Send a test pattern")
        print("\nFor help on a specific command, use: python -m ndirust_py command --help")
        
    return 0


if __name__ == '__main__':
    sys.exit(main()) 