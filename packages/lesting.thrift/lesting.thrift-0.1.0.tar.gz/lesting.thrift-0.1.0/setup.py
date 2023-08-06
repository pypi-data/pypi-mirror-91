from setuptools import setup, find_namespace_packages

setup(
    name = "lesting.thrift",
    version = "0.1.0",
    description = "Lesting Apache Thrift",
    url = "https://github.com/LESTINGX/THRIFT",
    packages = find_namespace_packages(exclude=("examples",)),
    namespace_packages = ["lesting"],
    install_requires = [
        "thriftpy2",
        "lesting.http"
    ],
    classifiers = [
        "License :: OSI Approved :: MIT License",
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