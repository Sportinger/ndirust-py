// src/sender.rs

use pyo3::prelude::*;
use ndi;
use pyo3::exceptions::PyRuntimeError;
use pyo3::types::PyBytes;

/// Python class for creating and sending NDI video frames
#[pyclass(unsendable)]  // Mark as unsendable to avoid thread safety concerns
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
                    .ndi_name(name.to_string())
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

    /// Send a test pattern video frame
    /// 
    /// Args:
    ///     width: Width of the test pattern (default: 1280)
    ///     height: Height of the test pattern (default: 720)
    ///     fps_n: Framerate numerator (default: 30)
    ///     fps_d: Framerate denominator (default: 1)
    #[pyo3(signature = (width=1280, height=720, fps_n=30, fps_d=1))]
    fn send_test_pattern(&self, width: u32, height: u32, fps_n: u32, fps_d: u32) -> PyResult<()> {
        let sender = match &self.sender {
            Some(s) => s,
            None => return Err(PyRuntimeError::new_err("Sender is not initialized")),
        };
        
        // Create a simple color test pattern in UYVY format (2 bytes per pixel)
        let data_size = (width * height * 2) as usize;
        let mut data = vec![0u8; data_size];
        
        // Create a colorful test pattern
        for y in 0..height {
            for x in 0..width {
                let index = ((y * width + x) * 2) as usize;
                if index + 1 < data_size {
                    // U and V values for color
                    data[index] = ((x * 255) / width) as u8;     // U: blue-difference chroma
                    data[index + 1] = ((y * 255) / height) as u8; // Y: luma
                    // Additional Y and V values
                    if x % 2 == 0 && index + 3 < data_size {
                        data[index + 2] = 128;   // V: red-difference chroma
                        data[index + 3] = 235;   // Y: luma (white)
                    }
                }
            }
        }
        
        // Create a video frame using the VideoData::from_buffer method
        let fourcc = ndi::FourCCVideoType::UYVY;
        let frame_format = ndi::FrameFormatType::Progressive;
        
        // Calculate stride (bytes per line)
        let stride = (width * 2) as i32;  // 2 bytes per pixel for UYVY
        
        // Create video frame
        let video_data = ndi::VideoData::from_buffer(
            width as i32, 
            height as i32,
            fourcc,
            fps_n as i32,
            fps_d as i32,
            frame_format,
            0, // timecode
            stride,
            None, // metadata
            &mut data
        );
        
        // Send the frame
        sender.send_video(&video_data);
        
        println!("Sent test pattern frame {}x{} @ {}/{} fps", width, height, fps_n, fps_d);
        Ok(())
    }
    
    /// Send custom video frame from raw byte data
    /// 
    /// Args:
    ///     data: Raw video data bytes
    ///     width: Width of the frame
    ///     height: Height of the frame
    ///     fps_n: Framerate numerator (default: 30)
    ///     fps_d: Framerate denominator (default: 1)
    #[pyo3(signature = (data, width, height, fps_n=30, fps_d=1))]
    fn send_video_frame(&self, data: &PyBytes, width: u32, height: u32, fps_n: u32, fps_d: u32) -> PyResult<()> {
        let sender = match &self.sender {
            Some(s) => s,
            None => return Err(PyRuntimeError::new_err("Sender is not initialized")),
        };
        
        // Extract bytes from PyBytes
        let mut py_bytes = Python::with_gil(|_py| {
            let bytes = data.as_bytes();
            bytes.to_vec()
        });
        
        // Calculate stride (bytes per line)
        let stride = (width * 2) as i32;  // 2 bytes per pixel for UYVY
        
        // Create video frame
        let video_data = ndi::VideoData::from_buffer(
            width as i32, 
            height as i32,
            ndi::FourCCVideoType::UYVY,
            fps_n as i32,
            fps_d as i32,
            ndi::FrameFormatType::Progressive,
            0, // timecode
            stride,
            None, // metadata
            &mut py_bytes
        );
        
        // Send the frame
        sender.send_video(&video_data);
        
        Ok(())
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