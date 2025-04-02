// src/receiver.rs

use pyo3::prelude::*;
use ndi;
use pyo3::exceptions::PyRuntimeError;
use pyo3::types::{PyBytes, PyDict};
use std::time::Duration;

/// Frame type enum exposed to Python
#[pyclass]
#[derive(Clone, Copy)]
pub enum FrameType {
    None = 0,
    Video = 1,
    Audio = 2,
    Metadata = 3,
    Error = 4,
}

/// Python class representing an NDI video frame
#[pyclass]
struct NdiVideoFrame {
    #[pyo3(get)]
    width: u32,
    
    #[pyo3(get)]
    height: u32,
    
    #[pyo3(get)]
    frame_rate_n: u32,
    
    #[pyo3(get)]
    frame_rate_d: u32,
    
    #[pyo3(get)]
    timecode: i64,
    
    #[pyo3(get)]
    data_size: usize,
    
    // We're keeping the frame data as a reference inside a PyBytes object
    data: Option<Py<PyBytes>>,
    
    // FourCC video format
    #[pyo3(get)]
    four_cc: u32,
}

#[pymethods]
impl NdiVideoFrame {
    #[new]
    #[pyo3(signature = (width, height, frame_rate_n, frame_rate_d, timecode, data_size, data = None, four_cc = 0))]
    fn new(
        width: u32,
        height: u32,
        frame_rate_n: u32,
        frame_rate_d: u32,
        timecode: i64,
        data_size: usize,
        data: Option<Py<PyBytes>>,
        four_cc: u32,
    ) -> Self {
        NdiVideoFrame {
            width,
            height,
            frame_rate_n,
            frame_rate_d,
            timecode,
            data_size,
            data,
            four_cc,
        }
    }

    /// Get a copy of the frame data
    fn get_data(&self, _py: Python<'_>) -> Option<Py<PyBytes>> {
        self.data.clone()
    }
    
    /// Get the FourCC format as a string
    fn get_four_cc_name(&self) -> String {
        match self.four_cc {
            0x59565955 => "UYVY".to_string(), // UYVY format
            0x41565559 => "UYVA".to_string(), // UYVA format
            0x36313250 => "P216".to_string(), // P216 format
            0x36314150 => "PA16".to_string(), // PA16 format
            0x32315659 => "YV12".to_string(), // YV12 format
            0x30323449 => "I420".to_string(), // I420 format
            0x3231564E => "NV12".to_string(), // NV12 format
            0x41524742 => "BGRA".to_string(), // BGRA format
            0x41424752 => "RGBA".to_string(), // RGBA format
            0x58524742 => "BGRX".to_string(), // BGRX format
            0x58424752 => "RGBX".to_string(), // RGBX format
            _ => format!("Unknown (0x{:08X})", self.four_cc),
        }
    }
}

/// Python class representing an NDI audio frame
#[pyclass]
struct NdiAudioFrame {
    #[pyo3(get)]
    sample_rate: u32,
    
    #[pyo3(get)]
    num_channels: u32,
    
    #[pyo3(get)]
    num_samples: u32,
    
    #[pyo3(get)]
    timecode: i64,
    
    #[pyo3(get)]
    data_size: usize,
    
    // We're keeping the audio data as a reference inside a PyBytes object
    data: Option<Py<PyBytes>>,
}

#[pymethods]
impl NdiAudioFrame {
    #[new]
    #[pyo3(signature = (sample_rate, num_channels, num_samples, timecode, data_size, data = None))]
    fn new(
        sample_rate: u32,
        num_channels: u32,
        num_samples: u32,
        timecode: i64,
        data_size: usize,
        data: Option<Py<PyBytes>>,
    ) -> Self {
        NdiAudioFrame {
            sample_rate,
            num_channels,
            num_samples,
            timecode,
            data_size,
            data,
        }
    }

    /// Get a copy of the audio data
    fn get_data(&self, _py: Python<'_>) -> Option<Py<PyBytes>> {
        self.data.clone()
    }
}

/// Python class representing an NDI metadata frame
#[pyclass]
struct NdiMetadataFrame {
    #[pyo3(get)]
    timecode: i64,

    #[pyo3(get)]
    data: String,
}

#[pymethods]
impl NdiMetadataFrame {
    #[new]
    fn new(timecode: i64, data: String) -> Self {
        NdiMetadataFrame {
            timecode,
            data,
        }
    }
}

/// Python class representing an NDI receiver
#[pyclass]
struct NdiReceiver {
    receiver: Option<ndi::recv::Recv>,
    connected_source: Option<String>,
}

#[pymethods]
impl NdiReceiver {
    #[new]
    fn new() -> PyResult<Self> {
        // Initialize NDI if not already initialized
        match ndi::initialize() {
            Ok(_) => {
                // Create an unconnected receiver
                let recv_builder = ndi::recv::RecvBuilder::new();
                let recv_create = recv_builder.build();
                
                match recv_create {
                    Ok(receiver) => Ok(NdiReceiver { 
                        receiver: Some(receiver),
                        connected_source: None,
                    }),
                    Err(_) => Err(PyRuntimeError::new_err("Failed to create NDI receiver")),
                }
            },
            Err(_) => Err(PyRuntimeError::new_err(
                "Failed to initialize NDI runtime. Make sure the NDI SDK is installed on your system.",
            )),
        }
    }

    /// Connect to an NDI source
    fn connect_to_source(&mut self, source_name: &str) -> PyResult<()> {
        let receiver = match &mut self.receiver {
            Some(r) => r,
            None => return Err(PyRuntimeError::new_err("Receiver is not initialized")),
        };
        
        // Find the source with the given name
        let find_create = ndi::find::FindBuilder::new().build();
        match find_create {
            Ok(finder) => {
                // Look for sources with a reasonable timeout
                let sources_result = finder.current_sources(3000);
                
                match sources_result {
                    Ok(sources) => {
                        // Find the source with the matching name
                        for source in sources.iter() {
                            if source.get_name() == source_name {
                                // Connect to this source
                                receiver.connect(source);
                                self.connected_source = Some(source_name.to_string());
                                return Ok(());
                            }
                        }
                        
                        // If we get here, the source was not found
                        Err(PyRuntimeError::new_err(format!("Source not found: {}", source_name)))
                    },
                    Err(_) => Err(PyRuntimeError::new_err("Timeout while searching for sources")),
                }
            },
            Err(_) => Err(PyRuntimeError::new_err("Failed to create NDI finder")),
        }
    }

    /// Get the name of the connected source
    #[getter]
    fn get_connected_source(&self) -> Option<String> {
        self.connected_source.clone()
    }

    /// Receive a frame with a timeout
    fn receive_frame(&mut self, timeout_ms: Option<u32>, py: Python<'_>) -> PyResult<(FrameType, PyObject)> {
        let receiver = match &mut self.receiver {
            Some(r) => r,
            None => return Err(PyRuntimeError::new_err("Receiver is not initialized")),
        };
        
        // Default to 1 second timeout
        let timeout = timeout_ms.unwrap_or(1000); 
        
        // Create mutable options to hold the received frames
        let mut video_data = None;
        let mut audio_data = None;
        let mut metadata_data = None;
        
        // Capture a frame - ndi crate expects u128 value
        let frame_type = receiver.capture_all(
            &mut video_data,
            &mut audio_data,
            &mut metadata_data,
            timeout.into() // Convert u32 to u128
        );
        
        // Convert the frame type to our enum
        let frame_type_py = match frame_type {
            ndi::FrameType::Video => FrameType::Video,
            ndi::FrameType::Audio => FrameType::Audio,
            ndi::FrameType::Metadata => FrameType::Metadata,
            ndi::FrameType::None => FrameType::None,
            _ => FrameType::Error, // Handle any other cases
        };
        
        // Process the received frame based on its type
        match frame_type_py {
            FrameType::Video => {
                // We received a video frame
                if let Some(video) = video_data {
                    let width = video.width() as u32;
                    let height = video.height() as u32;
                    let frame_rate_n = video.frame_rate_n() as u32;
                    let frame_rate_d = video.frame_rate_d() as u32;
                    let timecode = video.timecode();
                    
                    // Get the raw data pointer and size
                    let p_data = video.p_data();
                    let mut data_size = 0;
                    
                    // Determine the frame data size based on the format
                    if let Some(stride) = video.line_stride_in_bytes() {
                        data_size = (stride * height) as usize;
                    } else if let Some(size) = video.data_size_in_bytes() {
                        data_size = size as usize;
                    } else {
                        // If neither is available, calculate a reasonable default size
                        // For UYVY format, we need 2 bytes per pixel
                        data_size = (width as usize * height as usize * 2) as usize;
                    }
                    
                    // Create a PyBytes object with the video data
                    let data_bytes = unsafe {
                        PyBytes::from_ptr(py, p_data as *const u8, data_size)
                    };
                    
                    // Create an NdiVideoFrame object with the frame data
                    let frame = NdiVideoFrame::new(
                        width,
                        height,
                        frame_rate_n,
                        frame_rate_d,
                        timecode,
                        data_size,
                        Some(data_bytes.into_py(py)),
                        video.four_cc() as u32,
                    );
                    
                    return Ok((frame_type_py, Py::new(py, frame)?.into_py(py)));
                }
            },
            FrameType::Audio => {
                // We received an audio frame
                if let Some(audio) = audio_data {
                    let sample_rate = audio.sample_rate() as u32;
                    let num_channels = audio.no_channels() as u32;
                    let num_samples = audio.no_samples() as u32;
                    let timecode = audio.timecode();
                    
                    // Get the audio data size (samples * channels * 4 bytes per float)
                    let data_size = (num_samples as usize * num_channels as usize * 4) as usize;
                    
                    // Create a PyBytes object with the audio data
                    let data_bytes = unsafe {
                        PyBytes::from_ptr(py, audio.p_data() as *const u8, data_size)
                    };
                    
                    // Create an NdiAudioFrame object with the frame data
                    let frame = NdiAudioFrame::new(
                        sample_rate,
                        num_channels,
                        num_samples,
                        timecode,
                        data_size,
                        Some(data_bytes.into_py(py)),
                    );
                    
                    return Ok((frame_type_py, Py::new(py, frame)?.into_py(py)));
                }
            },
            FrameType::Metadata => {
                // We received a metadata frame
                if let Some(metadata) = metadata_data {
                    let timecode = metadata.timecode();
                    let data = metadata.data();
                    
                    // Create an NdiMetadataFrame object with the frame data
                    let frame = NdiMetadataFrame::new(
                        timecode,
                        data,
                    );
                    
                    return Ok((frame_type_py, Py::new(py, frame)?.into_py(py)));
                }
            },
            _ => {}
        }
        
        // If we get here, we either got an empty frame or an error
        Ok((frame_type_py, py.None()))
    }

    /// Close the receiver and free resources
    fn close(&mut self) -> PyResult<()> {
        self.receiver = None;
        self.connected_source = None;
        Ok(())
    }
}

/// Register receiver-related Python functions and classes
pub fn register_receiver_functions(m: &PyModule) -> PyResult<()> {
    m.add_class::<FrameType>()?;
    m.add_class::<NdiVideoFrame>()?;
    m.add_class::<NdiAudioFrame>()?;
    m.add_class::<NdiMetadataFrame>()?;
    m.add_class::<NdiReceiver>()?;
    
    Ok(())
} 