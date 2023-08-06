from setuptools import setup, find_namespace_packages

setup(
    name = "lesting.http",
    version = "0.1.0",
    description = "A comprehensive HTTP client",
    url = "https://github.com/LESTINGX/HTTP",
    packages = find_namespace_packages(),
    namespace_packages = ["lesting"],
    install_requires = [
        "httplib2"
    ],
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    zip_safe = False
)