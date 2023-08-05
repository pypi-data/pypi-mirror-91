from setuptools import setup, find_namespace_packages

setup(
    name = "lesting.api",
    version = "0.0.1",
    description = "Lesting API discovery",
    url = "https://github.com/LESTINGT/API",
    packages = find_namespace_packages(exclude=("examples",)),
    namespace_packages = ["lesting"],
    install_requires = [
        "httplib2"
    ],
    classifiers = [
        "License :: OSI Approved :: BSD License",
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