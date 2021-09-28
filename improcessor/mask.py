#=========================== improcessor_mask ===========================
#
# @class        improcessor.mask
#
# @brief        A generic class that simplifies applying basic 
#               processing to a binary mask.  
#
#
# The basic idea is the ability to specify a series of binary mask processing
# functions in order to convert it from one mask representation to
# another like a sequential chain of signal processing operations
# 
# The basic operations include (but not limited to) the following
# connected components analysis or morphological techniques: 
# 1. getLargestCC (get the largest connected components) 
# 2. erode
# 3. dilate
# 4. opening(erode then dilate)
# 5. closing(dilate then erode)
#
# The arguments should be passed in pairs with the processing
# technique to be passed as a function pointer then optional arguments
# (this must be a tuple).  It is assumed that the processing will
# function as follows: 
#
# > newmask = technique(mask, optargs)
#
# If there are no optional arguments, then do not pass anything.
#
# Possible functions include any function that exists in the class
# invocation or function setting scope.
#
#
#  IMPLEMENTATION:
#
# ```
#  import improcessor.mask as maskprocessor
#
#  maskproc = maskprocessor.basic(options)
#
#  ...
#
#  newMask = maskproc.apply(mask)
#
#  ...
# ```
#
#  EXAMPLES:
#
#  After importing the maskprocessor, to keep only the largest connected components,
#  one would initialize as:
#
#  > maskprocessor = maskprocessor.basic(improcessor.mask.getLargestCC,()))
#
#  To additionally apply the morphological opening, one can change the initialization to:
#
#  > maskprocessor = maskprocessor.basic(improcessor.mask.getLargestCC,(), improcessor.mask.opening, (kernel,))
#
#! NOTE:
#!  indent is set to 2 spaces.
#!  tab is set to 4 spaces with conversion.
#
#
#=========================== improcessor.mask ===========================

#
# @file     mask.py
#
# @author   Yiye Chen,          yychen2019@gatech.edu
# 
# @date     2021/09/28 [created]
#
#=========================== improcessor.mask ===========================

import numpy as np
import inspect
import types
from skimage.measure import label

import cv2

from improcessor.basic import basic

class mask(basic):

  def __init__(self, *args):
      super().__init__(*args)
    
  #=============================== apply ===============================
  #
  # @brief  Execute the mask processing sequence.
  #
  # @param[in]  mask      The mask to process.
  # @param[out] maskOut   The processed mask.
  #
  def apply(self, mask):
  
    if mask is None or self.numfuncs == 0:
      maskOut = None

    if self.numfuncs > 0:
      # sanity check that input is a binary mask
      assert len(mask.shape) == 2 and (mask.dtype == bool), \
        "The input mask is expected to be a binary array with the shape like (H, W), \
        now the input dtype and shape are: {} and {}".format(mask.dtype, mask.shape)
      maskOut = np.copy(mask)
      for ii in range(self.numfuncs):
        if not self.methods[ii][1]:             # w/o parameter
          maskOut = self.methods[ii][0](maskOut)
        else:                                   # w/ parameter
          maskOut = self.methods[ii][0](maskOut, *self.methods[ii][1])

    return maskOut
  
  @staticmethod
  def getLargestCC(mask):
    """Return the largest connected component of a binary mask
    If the mask has no connected components (all zero), will be directly returned

    @param[in]      mask                    The input binary mask
    @param[out]     largestCC               The binary mask of the largest connected component
                                            The shape is the same as the input mask
    """
    labels = label(mask)
    if labels.max() == 0:
        Warning("The input mask has no connected component. \
            Will be directly returned")
        largestCC = mask
    else:
        largestCC = labels == np.argmax(np.bincount(labels.flat)[1:])+1
    return largestCC

  @staticmethod
  def erode(mask, kernel):
    """Morphological erosion operation

    Args:
        mask (np.ndarray. (H, W)): The input mask
        kernel (np.ndarray. (Hk, Wk)): The kernel for morphological erosion
    
    Returns:
        maskErode (np.ndarray. (H, W)): The mask after erosion
    """
    maskErode = cv2.erode(mask.astype(np.uint8), kernel).astype(bool)
    return maskErode
  
  @staticmethod
  def dilate(mask, kernel):
    """Morphological dilation operation

    Args:
        mask (np.ndarray. (H, W)): The input mask
        kernel (np.ndarray. (Hk, Wk)): The kernel for morphological dilation

    Returns:
        maskDilate [np.ndarray. (H, W)]: The mask after dilation
    """
    maskDilate =cv2.dilate(mask.astype(np.uint8), kernel).astype(bool)
    return maskDilate

  @staticmethod
  def opening(mask, kernel):
    """Morphological opening operation

    Args:
        mask (np.ndarray. (H, W)): The input mask
        kernel (np.ndarray. (Hk, Wk)): The kernel for morphological opening

    Returns:
        maskOpening [np.ndarray. (H, W)]: The mask after Opening operation
    """
    maskOpening = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_OPEN, kernel).astype(bool)
    return maskOpening

  @staticmethod
  def closing(mask, kernel):
    """Morphological opening operation

    Args:
        mask (np.ndarray. (H, W)): The input mask
        kernel (np.ndarray. (Hk, Wk)): The kernel for morphological closing

    Returns:
        maskClosing [np.ndarray. (H, W)]: The mask after Closing operation
    """
    maskClosing = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_CLOSE, kernel).astype(bool)
    return maskClosing 
