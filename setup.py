from setuptools import setup, find_packages

setup(
    name="alphaSim",
    version="0.1.0",
    description="3D sensor simulation for Washington, DC",
    author="",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "matplotlib>=3.7.0",
    ],
    python_requires=">=3.8",
)
