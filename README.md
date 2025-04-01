# ndirust-py: Python NDI Bindings

This project provides Python bindings for NewTek's NDI® (Network Device Interface) technology using Rust via PyO3.

## Features

- NDI source discovery on the network
- Receiving NDI video, audio, and metadata 
- Sending NDI video, audio, and metadata
- Cross-platform support (Windows, macOS, Linux)

## Requirements

- Python 3.7 or higher
- [NDI SDK](https://ndi.tv/tools/) installed on your system
- Rust compiler (for building)

## Installation

1. Install the NDI SDK from https://ndi.tv/tools/
2. Make sure you have a Rust compiler installed
3. Install the package using pip:

```bash
pip install ndirust-py
```

Or install from source:

```bash
git clone https://github.com/yourusername/ndirust-py.git
cd ndirust-py
pip install maturin
maturin develop
```

## Quick Examples

### Finding NDI Sources

```python
import ndirust_py

# Initialize NDI
ndirust_py.initialize_ndi()

# Create a finder
finder = ndirust_py.discovery.NdiFinder()

# Get available sources (with 1 second timeout)
sources = finder.find_sources(timeout_ms=1000)

# Print sources
for source in sources:
    print(f"Found source: {source.name} at {source.address}")
```

### Sending NDI Video

```python
import ndirust_py
import time

# Initialize NDI
ndirust_py.initialize_ndi()

# Create a sender
sender = ndirust_py.sender.NdiSender("My Python NDI Sender")

# Create a simple test frame (UYVY format)
width, height = 1280, 720
frame_data = bytes([128, 255, 128, 255] * (width * height // 2))  # Simple UYVY pattern

# Send the frame
sender.send_video(
    data=frame_data,
    width=width, 
    height=height,
    frame_rate_n=30,  # 30fps
    frame_rate_d=1,
    fourcc="UYVY"
)

# Wait a bit to ensure the frame is sent
time.sleep(0.1)
```

### Receiving NDI Video

```python
import ndirust_py
from ndirust_py.receiver import FrameType

# Initialize NDI
ndirust_py.initialize_ndi()

# Create a receiver
receiver = ndirust_py.receiver.NdiReceiver()

# Connect to a specific source (first find it)
finder = ndirust_py.discovery.NdiFinder()
sources = finder.find_sources(timeout_ms=1000)

if sources:
    # Connect to the first source
    receiver.connect_to_source(sources[0].name)
    
    # Receive a frame with a timeout
    frame_type, frame_data = receiver.receive_frame(timeout_ms=5000)  # 5 second timeout
    
    if frame_type == FrameType.Video:
        print(f"Received video frame: {frame_data.width}x{frame_data.height}")
        
        # Process the frame data
        raw_data = frame_data.get_data()  # Get the raw frame data as bytes
```

## API Reference

The library provides the following modules:

- `ndirust_py` - Core functionality and utilities
- `ndirust_py.discovery` - Finding NDI sources on the network
- `ndirust_py.sender` - Sending NDI video, audio, and metadata
- `ndirust_py.receiver` - Receiving NDI video, audio, and metadata

See the [examples/](examples/) directory for complete examples.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [NewTek NDI®](https://ndi.tv/) is a registered trademark of NewTek, Inc.
- [ndi crate](https://docs.rs/ndi/latest/ndi/) provides the underlying Rust bindings
- [PyO3](https://pyo3.rs) enables the Rust to Python bindings

## Project Status

This project is currently in active development. 