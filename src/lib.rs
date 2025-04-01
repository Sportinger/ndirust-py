mod discovery;
mod receiver;
mod sender;
mod utils;

use pyo3::prelude::*;
use pyo3::exceptions::PyRuntimeError;
use pyo3::types::PyDict;

// Function to provide version information
#[pyfunction]
fn get_version_info() -> PyResult<String> {
    Ok("NDI Rust Python bindings v0.1.0".to_string())
}

// Simple test function to verify Python binding works
#[pyfunction]
fn test_binding() -> PyResult<bool> {
    Ok(true)
}

/// A Python module implemented in Rust.
#[pymodule]
fn ndirust_py(_py: Python, m: &PyModule) -> PyResult<()> {
    // Add core functions
    m.add_function(wrap_pyfunction!(get_version_info, m)?)?;
    m.add_function(wrap_pyfunction!(test_binding, m)?)?;

    // Add submodules
    let discovery_module = PyModule::new(_py, "discovery")?;
    discovery::register_discovery_functions(discovery_module)?;
    m.add_submodule(discovery_module)?;

    let receiver_module = PyModule::new(_py, "receiver")?;
    receiver::register_receiver_functions(receiver_module)?;
    m.add_submodule(receiver_module)?;

    let sender_module = PyModule::new(_py, "sender")?;
    sender::register_sender_functions(sender_module)?;
    m.add_submodule(sender_module)?;

    // Add module-level attributes
    let sys = PyModule::import(_py, "sys")?;
    let version = get_version_info()?;
    let locals = PyDict::new(_py);
    locals.set_item("sys", sys)?;
    locals.set_item("version", version)?;

    Ok(())
}
