#=========================== improcessor_basic ===========================
#
# @class        improcessor.basic
#
# @brief        A generic class that simplifies applying basic image
#               processing to an image.  
#
#
# The basic idea is the ability to specify a series of image processing
# functions in order to convert it from one image representation to
# another like a sequential chain of signal processing operations
#
# Basic manipulations include scaling, clipping, normalization, and
# resizing.  What to do is specified by the arguments of the initial
# function call.  If the arguments are empty, then it will do nothing.
# The order of the arguments makes a difference operationally, as
# improcessor will perform the processing in precisely that order.
#
# The arguments should be passed in pairs as technique/function name
# then optional arguments (this must be a tuple).  It is assumed
# that the processing will function as follows: 
#
# > newimage = technique(image, optargs)
#
# If there are no optional arguments, then pass an empty list (this
# works for the built-in options.)
# Possible functions are any function that Matlab has
# satifying the above implementation.  Some built-in options are:
#
#    newimage = builtin_clip(image, (minlimit maxlimit))
#    newimage = builtin_normalize(image)
#    newimage = builtin_scale(image, (minval maxval))
#    newimage = builtin_scaleabout(image, (anchorval diameter))
#
#
#  IMPLEMENTATION:
#
# ```
#  import improcessor.basic as improcessor
#
#  improc = improcessor.basic(options)
#
#  ...
#
#  newImage = improc.apply(Image)
#
#  ...
# ```
#
#  EXAMPLES:
#
#  To upsample an image to a desired size (x,y) using bilinear interpolation,
#  one would initialize as:
#
#  import improcessor.basic as improcessor
#  improcessor = improcessor.basic('imresize',(x,y))
#
#  To additionally clip the values to lie between 2 and 20 one would
#  modify the initialization to be:
#
#  improcessor = improcessor.basic('imresize',(x,y),'clip',(2 20))
#
# NOTE:
# 
# There are some difference between this Python version and the corresponding matlab source. Basically, it simplifies some implementations, including basic stuff, reset, and free. 
#
#
#=========================== improcessor.basic ===========================

#
# @file     basic.py
#
# @author   Patricio A. Vela, pvela@gatech.edu
# @author   Yunzhi Lin, yunzhi.lin@gatech.edu
# 
# @date     2021/07/03 [created]
# @date     2021/07/07 [modified]
#
#=========================== improcessor.basic ===========================
import cv2
import numpy as np

# @classf improcessor
class basic(object):

  def __init__(self, *args):

    self.args = args
    self.numfuncs = 0
    self.methods  = []
    self.ignore_undef = False      #< Ignore undefined functions?
    self._setProcess()

  #------------------------------- _setProcess ------------------------------
  #
  #  @brief Set the processing methods.  Wipes pre-existing values. Mostly used to intialize numfuncs and methods.
  #  
  def _setProcess(self):

    lasti = len(self.args)
    ind = 0

    while ind < lasti:
      # Todo: 
      # Not sure about the function of the codes below.
      # 
      # if isa(varargin[ind],'function_handle')
      #   numfuncs = numfuncs+1
      #   methods{numfuncs} = {func2str(self.args{ind}), self.args{ind+1}}
      # else:

      if self.args[ind] == 'clip' or self.args[ind] == 'scale' or self.args[ind] == 'scaleabout' :
        self.methods.append([f'_builtin_{self.args[ind]}',self.args[ind+1]])
        self.numfuncs = self.numfuncs+1
      elif self.args[ind] == 'normalize':
        self.methods.append(['_builtin_normalize', []])
        self.numfuncs = self.numfuncs+1
      else:
        # Todo:
        # Have something to do with the official build-in functions in MATLAB. See https://www.mathworks.com/help/matlab/ref/exist.html?searchHighlight=exist&s_tid=srchtitle
        #
        # if ismember(exist(self.args[ind]), [2 3 5 6]):
        #   self.numfuncs = self.numfuncs+1
        #   self.methods[self.numfuncs] = [self.args[ind], self.args[ind+1]]

        if self.args[ind] == 'imresize':
          # FIXME:
          # Use OpenCV functions instead?
          self.methods.append(['imresize',self.args[ind+1]])
          self.__setattr__('imresize',cv2.resize)
          self.numfuncs = self.numfuncs+1
        elif not self.ignore_undef:
          print(f'Unknown option (\' {self.args[ind]} \'), ignoring')

      ind = ind+2

  #================================ set ================================
  #
  # @brief  Set parameters/member variables of the improcessor.
  #

  def set(self, fname, args):

    if fname == 'ignore':
      # args = True or False
      self.ignore_undef = args
    elif fname == 'processing':
        self.args = args
        self._setProcess()

  #================================ get ================================
  #
  # @brief  Get parameters/member variables of the improcessor.
  #

  def get(self, fname, args):

    if fname == 'ignore':
      fval = self.ignore_undef
    elif fname == 'processing':
      fval = self.methods

    return fval

  #=============================== apply ===============================
  #
  # @brief  Execute the image processing sequence.
  #
  # @param[in]  image   The image to process.
  # @param[out] imout   The processed image.
  
  def apply(self, image):
  
    if image is None or self.numfuncs == 0:
      imout = None

    if self.numfuncs > 0:
      imout = np.copy(image)
      for ii in range(self.numfuncs):
        if not self.methods[ii][1]:
          # w/o parameter
          imout = getattr(self, self.methods[ii][0])(imout)
        else:
          # w/ parameter
          imout = getattr(self, self.methods[ii][0])(imout, self.methods[ii][1])

    return imout

  #================================ post ===============================
  #
  # @brief  Execute post-processing of given image.
  #
  # @param[in]  image   The image to process.
  # @param[out] imout   The processed image.
  
  def post(self, image):
    
    # Default is to do nothing. Overload to get less "basic."
    
    raise NotImplementedError

  def _builtin_clip(self, img, limits):
    return builtin_clip(img, limits)
  def _builtin_normalize(self, img, empty):
    return builtin_normalize(img, empty)
  def _builtin_scale(self, img, scparms):
    return builtin_clip(img, scparms)
  def _builtin_scaleabout(self, img, scparms):
    return builtin_clip(img, scparms)

#============================= builtin_clip ============================
#
def builtin_clip(img, limits):

  img = np.array(img)
  nimg = np.clip(img, limits[0], limits[1])

  return nimg

#========================== builtin_normalize ==========================
#
def builtin_normalize(img, empty):

  img = np.array(img)
  minI = np.min(img, axis=2)
  maxI = np.max(img, axis=2)
  nimg = (img-minI)/(maxI-minI)

  return nimg


#============================ builtin_scale ============================
#
def builtin_scale(img, scparms):

  img = np.array(img)
  minI = np.min(img, axis=2)
  maxI = np.max(img, axis=2)
  nimg = (scparms[1]-scparms[0])*(img-minI)/(maxI-minI) + scparms[0]

  return nimg

#========================== builtin_scaleabout =========================
#
def builtin_scaleabout(img, scparms):

  img = np.array(img)
  minI = np.min(img, axis=2)
  maxI = np.max(img, axis=2)
  nimg = scparms[1]*(img-minI)/(maxI-minI) + scparms[0] - scparms[1]/2

  return nimg