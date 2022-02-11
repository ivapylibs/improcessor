from setuptools import setup
setup(name='improcessor',
      version='1.0',
      description='Classes implementing flexible and run-time specifiable image processing pipelines.', 
      author='IVALab',
      packages=['improcessor'],
      install_requires=['improcessor', 'numpy', 'matplotlib', 'opencv-python', 'scikit-image'],
      )
