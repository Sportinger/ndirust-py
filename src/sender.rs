// src/sender.rs

use pyo3::prelude::*;
use ndi;
use pyo3::exceptions::PyRuntimeError;
use pyo3::types::PyBytes;
use std::time::Duration;

/// Python class for creating and sending NDI video frames
#[pyclass]
struct NdiSender {
    sender: Option<ndi::send::Send>,
    name: String,
}

#[pymethods]
impl NdiSender {
    #[new]
    fn new(name: &str) -> PyResult<Self> {
        // Initialize NDI if not already initialized
        match ndi::initialize() {
            Ok(_) => {
                let sender_create = ndi::send::SendBuilder::new()
                    .ndi_name(name)
                    .build();

                match sender_create {
                    Ok(sender) => Ok(NdiSender { 
                        sender: Some(sender),
                        name: name.to_string(),
                    }),
                    Err(_) => Err(PyRuntimeError::new_err("Failed to create NDI sender")),
                }
            },
            Err(_) => Err(PyRuntimeError::new_err(
                "Failed to initialize NDI runtime. Make sure the NDI SDK is installed on your system.",
            )),
        }
    }

    /// Send a video frame
    #[pyo3(signature = (data, width, height, frame_rate_n=30, frame_rate_d=1, fourcc="UYVY", aspect_ratio=16.0/9.0))]
    fn send_video(&self, data: &PyBytes, width: i32, height: i32, frame_rate_n: i32, frame_rate_d: i32, 
                 fourcc: &str, aspect_ratio: f32) -> PyResult<()> {
        let sender = match &self.sender {
            Some(s) => s,
            None => return Err(PyRuntimeError::new_err("Sender is not initialized")),
        };
        
        // Extract frame data from PyBytes
        let frame_data = data.as_bytes();
        
        // Create a video frame
        let mut video_frame = ndi::VideoData {
            width,
            height,
            frame_rate_n,
            frame_rate_d,
            picture_aspect_ratio: aspect_ratio,
            frame_format_type: ndi::FrameFormatType::Progressive,
            timecode: ndi::send::TIMECODE_AUTO, // Let NDI handle the timecode
            line_stride_in_bytes: 0, // Let NDI calculate based on width
            data: frame_data.to_vec(),
            fourcc: match fourcc {
                "RGBA" => ndi::FourCCVideoType::RGBA,
                "RGBX" => ndi::FourCCVideoType::RGBX,
                "BGRA" => ndi::FourCCVideoType::BGRA,
                "BGRX" => ndi::FourCCVideoType::BGRX,
                "UYVY" => ndi::FourCCVideoType::UYVY,
                _ => return Err(PyRuntimeError::new_err(format!("Unsupported fourcc: {}", fourcc))),
            },
            p_metadata: None,
        };
        
        // Send the video frame
        match sender.send_video(&mut video_frame) {
            Ok(_) => Ok(()),
            Err(_) => Err(PyRuntimeError::new_err("Failed to send video frame")),
        }
    }
    
    /// Send an audio frame
    #[pyo3(signature = (data, sample_rate=48000, num_channels=2, num_samples=1024))]
    fn send_audio(&self, data: &PyBytes, sample_rate: i32, num_channels: i32, num_samples: i32) -> PyResult<()> {
        let sender = match &self.sender {
            Some(s) => s,
            None => return Err(PyRuntimeError::new_err("Sender is not initialized")),
        };
        
        // Extract audio data from PyBytes
        let audio_bytes = data.as_bytes();
        
        // Convert the byte buffer to f32 samples (assuming correct format)
        let bytes_per_sample = std::mem::size_of::<f32>();
        let expected_size = (num_channels * num_samples) as usize * bytes_per_sample;
        
        if audio_bytes.len() != expected_size {
            return Err(PyRuntimeError::new_err(format!(
                "Audio data size mismatch: expected {} bytes, got {}", 
                expected_size, audio_bytes.len()
            )));
        }
        
        // Convert bytes to f32 samples
        let mut audio_data: Vec<f32> = Vec::with_capacity((num_channels * num_samples) as usize);
        for chunk in audio_bytes.chunks(bytes_per_sample) {
            if chunk.len() == bytes_per_sample {
                let sample = f32::from_le_bytes([chunk[0], chunk[1], chunk[2], chunk[3]]);
                audio_data.push(sample);
            }
        }
        
        // Create an audio frame
        let mut audio_frame = ndi::AudioData {
            sample_rate,
            no_channels: num_channels,
            no_samples: num_samples,
            timecode: ndi::send::TIMECODE_AUTO, // Let NDI handle the timecode
            data: audio_data,
            channel_stride_in_bytes: 0, // Let NDI calculate based on samples
            fourcc: ndi::FourCCAudioType::FloatLE, // Always using float samples
            p_metadata: None,
        };
        
        // Send the audio frame
        match sender.send_audio(&mut audio_frame) {
            Ok(_) => Ok(()),
            Err(_) => Err(PyRuntimeError::new_err("Failed to send audio frame")),
        }
    }
    
    /// Send a metadata frame
    fn send_metadata(&self, data: &str) -> PyResult<()> {
        let sender = match &self.sender {
            Some(s) => s,
            None => return Err(PyRuntimeError::new_err("Sender is not initialized")),
        };
        
        // Create a metadata frame
        let mut metadata_frame = ndi::MetaData {
            timecode: ndi::send::TIMECODE_AUTO, // Let NDI handle the timecode
            data: data.to_string(),
        };
        
        // Send the metadata frame
        match sender.send_metadata(&mut metadata_frame) {
            Ok(_) => Ok(()),
            Err(_) => Err(PyRuntimeError::new_err("Failed to send metadata")),
        }
    }
    
    /// Get the name of this NDI sender
    #[getter]
    fn get_name(&self) -> PyResult<String> {
        Ok(self.name.clone())
    }
    
    /// Close the sender and free resources
    fn close(&mut self) -> PyResult<()> {
        self.sender = None;
        Ok(())
    }
}

/// Register sender-related Python functions and classes
pub fn register_sender_functions(m: &PyModule) -> PyResult<()> {
    m.add_class::<NdiSender>()?;
    
    Ok(())
} 