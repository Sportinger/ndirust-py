# ndirust-py: Python NDI Bindings

This project provides Python bindings for NewTek's NDI® (Network Device Interface) technology using Rust via PyO3.

## Current Status

**This is a work in progress**. Due to API compatibility issues with the ndi crate, this implementation is currently simplified and only provides basic functionality.

- ✅ NDI initialization check
- ✅ Source discovery
- ⚠️ Receiver (limited implementation)
- ⚠️ Sender (placeholder implementation)

## Features

- NDI source discovery on the network
- Receiving NDI video, audio, and metadata (limited)
- Sending NDI video, audio, and metadata (placeholder)
- Cross-platform support (Windows, macOS, Linux)

## Requirements

- Python 3.7 or higher
- [NDI SDK](https://ndi.tv/tools/) installed on your system
- Rust compiler (for building)

## Installation

1. Install the NDI SDK from https://ndi.tv/tools/
2. Make sure you have a Rust compiler installed
3. Install from source:

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
    print(f"Found source: {source.name}")
```

### Current Issues and Next Steps

1. Proper handling of VideoData and AudioData structs in the ndi crate
2. Proper implementation of frame sending
3. Complete implementation of frame receiving
4. Metadata handling

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [NewTek NDI®](https://ndi.tv/) is a registered trademark of NewTek, Inc.
- [ndi crate](https://docs.rs/ndi/latest/ndi/) provides the underlying Rust bindings
- [PyO3](https://pyo3.rs) enables the Rust to Python bindings

## Project Status

This project is currently in active development. 