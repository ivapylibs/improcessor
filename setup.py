from setuptools import setup
setup(name='improcessor',
      version='1.0',
      description='Classes implementing flexible and run-time specifiable image processing pipelines.', 
      author='IVALab',
      packages=['improcessor'],
      install_requires=['numpy', 'matplotlib', 'opencv-contrib-python', 'scikit-image'],
      )
