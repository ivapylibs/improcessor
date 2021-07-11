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
# The arguments should be passed in pairs with the image processing
# technique to be passed as a function pointer then optional arguments
# (this must be a tuple).  It is assumed that the processing will
# function as follows: 
#
# > newimage = technique(image, optargs)
#
# If there are no optional arguments, then do not pass anything.
#
# Possible functions include any function that exists in the class
# invocation or function setting scope.
#
# Some built-in options are:
#
#    newimage = clip(image, (minlimit maxlimit))
#    newimage = normalize(image)
#    newimage = scale(image, (minval maxval))
#    newimage = scaleabout(image, (anchorval diameter))
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
#  After importing the improcessor, to upsample an image to a desired
#  size (x,y) using bilinear interpolation, one would initialize as:
#
#  > improcessor = improcessor.basic(cv2.resize,((x,y),))
#
#  To additionally clip the values to lie between 2 and 20 one would
#  modify the initialization to be:
#
#  > improcessor = #  improcessor.basic(cv2.resize,((x,y),),improcessor.basic.clip,((2 20),))
#
#! NOTE:
#!  indent is set to 2 spaces.
#!  tab is set to 4 spaces with conversion.
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

import numpy as np
import sys
import inspect
import types


# @classf improcessor
class basic(object):

  def __init__(self, *args):

    #self.args = args
    self.numfuncs = 0
    self.methods  = []
    self.mtype    = []
    self.ignore_undef = False
    self._setProcess(*args)

  #------------------------------- _setProcess ------------------------------
  #
  #  @brief Set the processing methods.  Wipes pre-existing values. Mostly used to intialize numfuncs and methods.
  #  
  def _setProcess(self, *args):

    lasti = len(args)
    ind = 0

    while ind < lasti:

      if callable(args[ind]) and not(inspect.isclass(args[ind])):
        self.methods.append([args[ind], args[ind+1]])
        self.mtype.append(1)
        self.numfuncs = self.numfuncs + 1

      elif not self.ignore_undef:
        print('Unknown option')
        #print(f'Unknown option (\' {self.args[ind]} \'), ignoring')
        #PAV doesn't have that python3 version yet. To fix soon.

      ind = ind+2

  #================================ set ================================
  #
  # @brief  Reset parameters/member variables of the improcessor.
  #
  #
  def set(self, fname, *args):

    if fname == 'ignore':
      # args = True or False
      self.ignore_undef = args
    elif fname == 'processing':
        self.args = args
        self.numfuncs = 0
        self.methods = []
        self.ignore_undef = False
        self._setProcess(*args)

  #================================ get ================================
  #
  # @brief  Get parameters/member variables of the improcessor.
  #
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
  #
  def apply(self, image):
  
    if image is None or self.numfuncs == 0:
      imout = None

    if self.numfuncs > 0:
      imout = np.copy(image)
      for ii in range(self.numfuncs):
        if not self.methods[ii][1]:             # w/o parameter
          imout = self.methods[ii][0](imout)
        else:                                   # w/ parameter
          imout = self.methods[ii][0](imout, *self.methods[ii][1])

    return imout

  #================================ post ===============================
  #
  # @brief  Execute post-processing of given image.
  #
  # Default for the basic class is to do nothing. Overload in subclass
  # to get less "basic" or more functionality.
  #
  # @param[in]  image   The image to process.
  # @param[out] image   The processed image.
  #
  def post(self, image):
    
    return image

  #================================ clip ===============================
  #
  @staticmethod
  def clip(img, limits):

    nimg = np.clip(img, limits[0], limits[1])
  
    return nimg


  #============================= clipTails =============================
  #
  # @brief  Clip the extremal values given as a percentage of the
  #         pixels in the image. Finds thresholds for the value at the
  #         x-percentile and the (1-x)-percentile, then applies them.
  #
  # @param[in]  img     The scalar valued image.
  #
  @staticmethod
  def clipTails(img, x):

    ivec = img.flatten()
    N    = ivec.size
    svec = np.sort(ivec) 

    Tlo = svec[int(N*.05)]
    Thi = svec[int(N*.95)]

    nimg = np.clip(img, Tlo, Thi);

    return nimg

  #============================= normalize =============================
  #
  @staticmethod
  def normalize(img):

    img = np.array(img)
    minI = np.min(img)
    maxI = np.max(img)
    nimg = (img-minI)/(maxI-minI)

    return nimg

  #=============================== scale ===============================
  #
  @staticmethod
  def scale(img, scparms):

    minI = np.min(img)
    maxI = np.max(img)
    nimg = (scparms[1]-scparms[0])*(img-minI)/(maxI-minI) + scparms[0]

    return nimg

  #============================= scaleabout ============================
  #
  @staticmethod
  def scaleabout(img, scparms):

    minI = np.min(img)
    maxI = np.max(img)
    nimg = scparms[1]*(img-minI)/(maxI-minI) + scparms[0] - scparms[1]/2

    return nimg
