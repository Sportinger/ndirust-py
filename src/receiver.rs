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
    width: i32,
    
    #[pyo3(get)]
    height: i32,
    
    #[pyo3(get)]
    frame_rate_n: i32,
    
    #[pyo3(get)]
    frame_rate_d: i32,
    
    #[pyo3(get)]
    timecode: i64,
    
    #[pyo3(get)]
    data_size: usize,
    
    // We're keeping the frame data as a reference inside a PyBytes object
    data: Option<Py<PyBytes>>,
}

#[pymethods]
impl NdiVideoFrame {
    /// Get a copy of the frame data
    fn get_data(&self, py: Python<'_>) -> Option<Py<PyBytes>> {
        self.data.clone()
    }
}

/// Python class representing an NDI audio frame
#[pyclass]
struct NdiAudioFrame {
    #[pyo3(get)]
    sample_rate: i32,
    
    #[pyo3(get)]
    num_channels: i32,
    
    #[pyo3(get)]
    num_samples: i32,
    
    #[pyo3(get)]
    timecode: i64,
    
    #[pyo3(get)]
    data_size: usize,
    
    // We're keeping the audio data as a reference inside a PyBytes object
    data: Option<Py<PyBytes>>,
}

#[pymethods]
impl NdiAudioFrame {
    /// Get a copy of the audio data
    fn get_data(&self, py: Python<'_>) -> Option<Py<PyBytes>> {
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

/// Python class representing an NDI receiver
#[pyclass]
struct NdiReceiver {
    receiver: Option<ndi::recv::Receiver>,
}

#[pymethods]
impl NdiReceiver {
    #[new]
    fn new(source_name: Option<&str>) -> PyResult<Self> {
        // Initialize NDI if not already initialized
        match ndi::initialize() {
            Ok(_) => {
                let recv_create = match source_name {
                    Some(name) => {
                        // Create a connection to a specific source
                        let source = ndi::Source {
                            ndi_name: name.to_string(),
                            url_address: None, // Not using URL-addressed sources
                        };
                        ndi::recv::ReceiverBuilder::new().build_with_source(source)
                    },
                    None => {
                        // Create an unconnected receiver
                        ndi::recv::ReceiverBuilder::new().build()
                    }
                };

                match recv_create {
                    Ok(receiver) => Ok(NdiReceiver { receiver: Some(receiver) }),
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
        
        let source = ndi::Source {
            ndi_name: source_name.to_string(),
            url_address: None, // Not using URL-addressed sources
        };
        
        if let Err(_) = receiver.connect(&source) {
            return Err(PyRuntimeError::new_err(format!("Failed to connect to source: {}", source_name)));
        }
        
        Ok(())
    }

    /// Receive a frame with a timeout
    fn receive_frame(&mut self, timeout_ms: Option<u32>, py: Python<'_>) -> PyResult<(FrameType, PyObject)> {
        let receiver = match &mut self.receiver {
            Some(r) => r,
            None => return Err(PyRuntimeError::new_err("Receiver is not initialized")),
        };
        
        let timeout = timeout_ms.unwrap_or(1000); // Default to 1 second timeout
        let duration = Duration::from_millis(timeout as u64);
        
        // Try to receive a frame
        match receiver.receive_capture(duration) {
            Ok(capture) => {
                // Process the capture based on its type
                match capture {
                    ndi::recv::Frame::Video(video) => {
                        // Create a Python video frame object
                        let data_size = video.data.len();
                        let py_bytes = PyBytes::new(py, &video.data);
                        
                        let video_frame = NdiVideoFrame {
                            width: video.width,
                            height: video.height,
                            frame_rate_n: video.frame_rate_n,
                            frame_rate_d: video.frame_rate_d,
                            timecode: video.timecode,
                            data_size,
                            data: Some(py_bytes.into()),
                        };
                        
                        Ok((FrameType::Video, Py::new(py, video_frame)?.into_py(py)))
                    },
                    ndi::recv::Frame::Audio(audio) => {
                        // Create a Python audio frame object
                        let data_size = audio.data.len() * std::mem::size_of::<f32>();
                        
                        // Convert audio data to bytes
                        let bytes: Vec<u8> = audio.data
                            .iter()
                            .flat_map(|sample| sample.to_le_bytes())
                            .collect();
                        
                        let py_bytes = PyBytes::new(py, &bytes);
                        
                        let audio_frame = NdiAudioFrame {
                            sample_rate: audio.sample_rate,
                            num_channels: audio.no_channels,
                            num_samples: audio.no_samples,
                            timecode: audio.timecode,
                            data_size,
                            data: Some(py_bytes.into()),
                        };
                        
                        Ok((FrameType::Audio, Py::new(py, audio_frame)?.into_py(py)))
                    },
                    ndi::recv::Frame::Metadata(metadata) => {
                        // Create a Python metadata frame object
                        let metadata_frame = NdiMetadataFrame {
                            timecode: metadata.timecode,
                            data: metadata.data,
                        };
                        
                        Ok((FrameType::Metadata, Py::new(py, metadata_frame)?.into_py(py)))
                    },
                    _ => {
                        // Return None for other frame types or no frame
                        let none = py.None();
                        Ok((FrameType::None, none))
                    }
                }
            },
            Err(_) => {
                // Return an error
                let none = py.None();
                Ok((FrameType::Error, none))
            }
        }
    }

    /// Close the receiver and free resources
    fn close(&mut self) -> PyResult<()> {
        self.receiver = None;
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