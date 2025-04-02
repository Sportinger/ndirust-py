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

    /// Send a video frame placeholder (this is a simplified version)
    #[pyo3(signature = (width=1280, height=720))]
    fn send_test_pattern(&self, width: u32, height: u32) -> PyResult<()> {
        let sender = match &self.sender {
            Some(s) => s,
            None => return Err(PyRuntimeError::new_err("Sender is not initialized")),
        };
        
        // Create a simple color test pattern
        let mut data = vec![0u8; (width * height * 2) as usize]; // UYVY format
        for i in 0..data.len() {
            data[i] = (i % 255) as u8;  // Simple pattern
        }
        
        // Create a video frame
        let mut video = ndi::VideoData::new();
        
        // Send the frame - this is simplified and may not work correctly
        println!("Pretending to send test pattern - feature in development");
        
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