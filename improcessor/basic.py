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
#  improcessor = improcessor.basic('resize',((x,y),))
#
#  To additionally clip the values to lie between 2 and 20 one would
#  modify the initialization to be:
#
#  improcessor = improcessor.basic('resize',((x,y),),'clip',((2 20),))
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
import sys
import inspect
import types
import operator
# @classf improcessor
class basic(object):

  def __init__(self, *args):

    self.args = args
    self.numfuncs = 0
    self.methods  = []
    self.ignore_undef = False
    self._setProcess()

  #------------------------------- _setProcess ------------------------------
  #
  #  @brief Set the processing methods.  Wipes pre-existing values. Mostly used to intialize numfuncs and methods.
  #  
  def _setProcess(self):

    lasti = len(self.args)
    ind = 0

    while ind < lasti:
      # @todo:
      # Currently, a function is implemented to check the locally defined functions.
      #
      # if isa(varargin[ind],'function_handle')
      #   numfuncs = numfuncs+1
      #   methods{numfuncs} = {func2str(self.args{ind}), self.args{ind+1}}
      #
      def is_local(object):
        return isinstance(object, types.FunctionType) and object.__module__ == __name__

      function_handle_list = [name for name, value in inspect.getmembers(sys.modules[__name__], predicate=is_local)]

      if self.args[ind] in function_handle_list:
        self.methods.append([self.args[ind], self.args[ind + 1]])
        self.numfuncs = self.numfuncs + 1
      elif self.args[ind] == 'clip' or self.args[ind] == 'scale' or self.args[ind] == 'scaleabout' :
        self.methods.append([f'builtin_{self.args[ind]}',self.args[ind+1]])
        self.numfuncs = self.numfuncs+1
      elif self.args[ind] == 'normalize':
        self.methods.append(['builtin_normalize', []])
        self.numfuncs = self.numfuncs+1
      elif self.args[ind] in dir(cv2):
        # Use OpenCV functions instead
        self.methods.append([f'cv2.{self.args[ind]}', self.args[ind + 1]])
        self.numfuncs = self.numfuncs + 1
      elif isinstance(self.args[ind], str):
        self.methods.append([self.args[ind], self.args[ind + 1]])
        self.numfuncs = self.numfuncs + 1
      # @todo:
      # The compiled function tests is ignored for now.
      #
      # if ismember(exist(self.args[ind]), [2 3 5 6]):
      #   self.numfuncs = self.numfuncs+1
      #   self.methods[self.numfuncs] = [self.args[ind], self.args[ind+1]]
      elif not self.ignore_undef:
        print(f'Unknown option (\' {self.args[ind]} \'), ignoring')

      ind = ind+2

  #================================ set ================================
  #
  # @brief  Reset parameters/member variables of the improcessor.
  #

  def set(self, fname, args):

    if fname == 'ignore':
      # args = True or False
      self.ignore_undef = args
    elif fname == 'processing':
        self.args = args
        self.numfuncs = 0
        self.methods = []
        self.ignore_undef = False
        self._setProcess()

  #================================ get ================================
  #
  # @brief  Get parameters/member variables of the improcessor.
  #

  def get(self, fname):

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
          imout = eval(self.methods[ii][0])(imout)
        else:
          # w/ parameter
          imout = eval(self.methods[ii][0])(imout, *self.methods[ii][1])

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