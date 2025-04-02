// src/discovery.rs

use pyo3::prelude::*;
use ndi;
use pyo3::exceptions::PyRuntimeError;
use pyo3::types::{PyDict, PyList};
use std::time::Duration;

/// Python class representing an NDI source
#[pyclass]
struct NdiSource {
    /// Source name
    #[pyo3(get)]
    name: String,
}

#[pymethods]
impl NdiSource {
    #[new]
    fn new(name: String) -> Self {
        NdiSource {
            name,
        }
    }

    fn __repr__(&self) -> String {
        format!("NdiSource(name='{}')", self.name)
    }
}

/// Python class representing an NDI finder
#[pyclass]
struct NdiFinder {
    finder: Option<ndi::find::Find>,
}

#[pymethods]
impl NdiFinder {
    #[new]
    fn new() -> PyResult<Self> {
        // Initialize the NDI system if not already initialized
        match ndi::initialize() {
            Ok(_) => {
                // Create a finder with default settings
                let find_create = ndi::find::FindBuilder::new().build();
                match find_create {
                    Ok(finder) => Ok(NdiFinder { finder: Some(finder) }),
                    Err(_) => Err(PyRuntimeError::new_err("Failed to create NDI finder")),
                }
            },
            Err(_) => Err(PyRuntimeError::new_err(
                "Failed to initialize NDI runtime. Make sure the NDI SDK is installed on your system.",
            )),
        }
    }

    /// Find all current NDI sources on the network
    fn find_sources(&self, timeout_ms: Option<u32>, py: Python<'_>) -> PyResult<Py<PyList>> {
        let finder = match &self.finder {
            Some(f) => f,
            None => return Err(PyRuntimeError::new_err("Finder is not initialized")),
        };
        
        // Get current sources with timeout
        let wait_ms = timeout_ms.unwrap_or(1000); // Default to 1 second timeout
        // current_sources expects a u128 value in milliseconds
        let sources_result = finder.current_sources(wait_ms as u128);
        
        // Convert to Python list
        let py_list = PyList::empty(py);
        
        // Process the result
        match sources_result {
            Ok(sources) => {
                // Process each found source
                for source in sources.iter() {
                    // Get the name from the source
                    let name = source.get_name();
                    
                    // Create a Python source object
                    let py_source = Py::new(py, NdiSource::new(name))?;
                    py_list.append(py_source)?;
                }
            },
            Err(_) => {
                // Timeout occurred, return empty list (this is not an error)
                println!("Find sources timeout occurred, no sources found.");
            }
        }
        
        Ok(py_list.into())
    }

    /// Free resources associated with the finder
    fn close(&mut self) -> PyResult<()> {
        self.finder = None;
        Ok(())
    }
}

/// Register discovery-related Python functions and classes
pub fn register_discovery_functions(m: &PyModule) -> PyResult<()> {
    m.add_class::<NdiSource>()?;
    m.add_class::<NdiFinder>()?;
    
    // Add function to check if NDI is supported on this CPU
    #[pyfunction]
    fn is_supported() -> bool {
        ndi::is_supported_CPU()
    }
    
    m.add_function(wrap_pyfunction!(is_supported, m)?)?;
    
    Ok(())
} 