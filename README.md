# ndirust-py: Python NDI Bindings

This project provides Python bindings for NewTek's NDI® (Network Device Interface) technology using Rust via PyO3.

## Features

- ✅ NDI initialization check
- ✅ Source discovery on the network
- ✅ Video frame sending
- ✅ Video frame receiving with full support for video, audio and metadata
- 🎁 Bundled NDI SDK DLLs - no separate installation needed!

## Requirements

- Python 3.7 or higher
- [NDI SDK](https://ndi.tv/tools/) installed on your system

## Installation

### Simple Installation

The package includes the necessary NDI runtime libraries, so you can simply install it with pip:

```bash
pip install ndirust-py
```

And you're ready to go! No need to download the NDI SDK separately.

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/ndirust-py.git
cd ndirust-py

# Install build dependencies
pip install maturin

# Build and install the package
maturin build --release
pip install target/wheels/ndirust_py-0.1.0-*.whl
```

## Using ndirust-py

### Finding NDI Sources

```python
import os
import ndirust_py

# Ensure NDI SDK DLL is in the PATH
ndi_sdk_path = r"C:\Program Files\NDI\NDI 6 SDK\Bin\x64"  # Adjust path as needed
os.environ["PATH"] = ndi_sdk_path + os.pathsep + os.environ["PATH"]

# Initialize NDI
ndirust_py.initialize_ndi()

# Create a finder
finder = ndirust_py.discovery.NdiFinder()

# Get available sources (with 1 second timeout)
sources = finder.find_sources(timeout_ms=1000)

# Print sources
for source in sources:
    print(f"Found source: {source}")

# Clean up
finder.close()
```

### Sending NDI Video

```python
import os
import time
import ndirust_py

# Ensure NDI SDK DLL is in the PATH
ndi_sdk_path = r"C:\Program Files\NDI\NDI 6 SDK\Bin\x64"  # Adjust path as needed
os.environ["PATH"] = ndi_sdk_path + os.pathsep + os.environ["PATH"]

# Initialize NDI
ndirust_py.initialize_ndi()

# Create an NDI sender
sender_name = "Python Test Sender"
sender = ndirust_py.sender.NdiSender(sender_name)

# Send a test pattern for 5 seconds
for i in range(150):  # 30fps * 5 seconds = 150 frames
    sender.send_test_pattern(width=1280, height=720, fps_n=30, fps_d=1)
    time.sleep(1/30)  # Sleep for approximately one frame duration

# Clean up
sender.close()
```

### Receiving NDI Video

```python
import time
import ndirust_py

# Initialize NDI
ndirust_py.initialize_ndi()

# First, find sources
finder = ndirust_py.discovery.NdiFinder()
sources = finder.find_sources(timeout_ms=3000)

if not sources:
    print("No NDI sources found!")
    finder.close()
    exit(1)

# Select the first source
source_name = str(sources[0]).replace("NdiSource(name='", "").replace("')", "")
print(f"Connecting to source: {source_name}")

# Create a receiver and connect to the source
receiver = ndirust_py.receiver.NdiReceiver()
receiver.connect_to_source(source_name)

# Receive frames for 10 seconds
start_time = time.time()
frame_count = 0

while time.time() - start_time < 10:
    # Receive a frame with 500ms timeout
    frame_type, frame = receiver.receive_frame(timeout_ms=500)
    
    # Check if we received a frame
    if frame_type == ndirust_py.receiver.FrameType.Video and frame is not None:
        frame_count += 1
        print(f"Video frame: {frame.width}x{frame.height} @ {frame.frame_rate_n}/{frame.frame_rate_d} fps")
        print(f"Format: {frame.get_four_cc_name()}")
    
    elif frame_type == ndirust_py.receiver.FrameType.Audio and frame is not None:
        print(f"Audio frame: {frame.sample_rate}Hz, {frame.num_channels} channels, {frame.num_samples} samples")
    
    elif frame_type == ndirust_py.receiver.FrameType.Metadata and frame is not None:
        print(f"Metadata: {frame.data[:50]}...")

print(f"Received {frame_count} frames in 10 seconds")

# Clean up
receiver.close()
finder.close()
```

## API Documentation

### Core Functions

- `ndirust_py.get_version_info()`: Get version information about the library
- `ndirust_py.initialize_ndi()`: Initialize the NDI runtime
- `ndirust_py.is_supported_cpu()`: Check if NDI is supported on this CPU

### Discovery Module

- `ndirust_py.discovery.NdiFinder()`: Create a new NDI finder
  - `find_sources(timeout_ms)`: Find NDI sources on the network
  - `close()`: Free resources

### Sender Module

- `ndirust_py.sender.NdiSender(name)`: Create a new NDI sender
  - `send_test_pattern(width, height, fps_n, fps_d)`: Send a test pattern frame
  - `send_video_frame(data, width, height, fps_n, fps_d)`: Send custom video data
  - `close()`: Free resources

### Receiver Module

- `ndirust_py.receiver.NdiReceiver()`: Create a new NDI receiver
  - `connect_to_source(source_name)`: Connect to a specific NDI source
  - `receive_frame(timeout_ms)`: Receive a frame (returns a tuple of frame_type and frame)
  - `close()`: Free resources

- Frame Types:
  - `ndirust_py.receiver.FrameType.None`: No frame received
  - `ndirust_py.receiver.FrameType.Video`: Video frame
  - `ndirust_py.receiver.FrameType.Audio`: Audio frame
  - `ndirust_py.receiver.FrameType.Metadata`: Metadata frame
  - `ndirust_py.receiver.FrameType.Error`: Error occurred

- Video Frames (`NdiVideoFrame`):
  - Properties: `width`, `height`, `frame_rate_n`, `frame_rate_d`, `timecode`, `data_size`, `four_cc`
  - Methods: `get_data()`, `get_four_cc_name()`

- Audio Frames (`NdiAudioFrame`):
  - Properties: `sample_rate`, `num_channels`, `num_samples`, `timecode`, `data_size`
  - Methods: `get_data()`

- Metadata Frames (`NdiMetadataFrame`):
  - Properties: `timecode`, `data`

## Project Status

This project is in active development but all major features are now implemented:

- ✅ Frame discovery
- ✅ Video sending
- ✅ Video receiving 
- ✅ Audio receiving
- ✅ Metadata receiving

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [NewTek NDI®](https://ndi.tv/) is a registered trademark of NewTek, Inc.
- [ndi crate](https://docs.rs/ndi/latest/ndi/) provides the underlying Rust bindings
- [PyO3](https://pyo3.rs) enables the Rust to Python bindings 