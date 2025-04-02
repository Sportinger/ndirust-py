from setuptools import setup

setup(
    name="ndirust-py",
    version="0.1.0",
    description="Python bindings for NewTek NDI using Rust",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="NDI Rust Python Bindings Team",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/ndirust-py",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Rust",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    keywords="ndi, video, rust, bindings",
    # The package will actually be built by maturin, so we don't specify packages here
) 