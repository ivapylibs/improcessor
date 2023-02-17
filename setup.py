from setuptools import setup, find_packages

setup(
    name="improcessor",
    version="1.0.1",
    description="Classes implementing flexible and run-time specifiable image processing pipelines.",
    author="IVALab",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "opencv-contrib-python",
        "scikit-image",
    ],
)
