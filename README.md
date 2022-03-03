# improcessors
Abstracted interface for image processing pipeline;  when basic image manipulation  needed before actual processing.

## Install

```
git clone git@github.com:ivapylibs/improcessor.git
pip3 install -e improcessor/
```

The test files are shell command line executable and should work when
invoked, presuming that pip installation has been performed.  If no
modifications to the source code will be performed then the ``-e`` flag
is not necessary (e.g., use the flag if the underlying code will be
modified).

## Dependencies

Requires the installation of the following python packages:

- ```numpy```
- ```opencv-contrib-python```
- ```matplotlib```
- ```scikit-image```
