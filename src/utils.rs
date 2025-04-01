// src/utils.rs

use pyo3::prelude::*;
use ndi; // Use the ndi crate directly 

/// Register utility functions for NDI API
pub fn register_utility_functions(m: &PyModule) -> PyResult<()> {
    // Add version information function
    #[pyfunction]
    fn get_ndi_version() -> String {
        // This is a placeholder since we can't directly get the SDK version
        // from the Rust API without initializing. Would normally call something like
        // ndi::version_string() or similar.
        "NDI SDK (via Rust bindings)".to_string()
    }
    
    // Add function to check if NDI is supported on this CPU
    #[pyfunction]
    fn is_supported_cpu() -> bool {
        ndi::is_supported_CPU()
    }
    
    // Add function to initialize NDI
    #[pyfunction]
    fn initialize_ndi() -> PyResult<bool> {
        match ndi::initialize() {
            Ok(_) => Ok(true),
            Err(_) => Ok(false),
        }
    }
    
    // Register the functions with the module
    m.add_function(wrap_pyfunction!(get_ndi_version, m)?)?;
    m.add_function(wrap_pyfunction!(is_supported_cpu, m)?)?;
    m.add_function(wrap_pyfunction!(initialize_ndi, m)?)?;
    
    Ok(())
} 