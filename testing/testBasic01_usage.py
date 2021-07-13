#!/usr/bin/python3
#=========================== testBasic01_usage ===========================
#
# @brief    Code to create an image interface and then use it to process
#           the source image. Use built-in functions.
#
#=========================== testBasic01_usage ===========================

#
# @file     testBasic01_usage.py
#
# @author   Yunzhi Lin, yunzhi.lin@gatech.edu
# @date     2021/07/08 [created]
#
#!NOTE:
#!  Indent is set to 2 spaces.
#!  Tab is set to 4 spaces with conversion to spaces.
#
# @quit
#=========================== testBasic01_usage ===========================

#==[0] Prep environment
#
import numpy as np
import operator
import improcessor.basic as improcessor


def runTest():
  image = np.zeros((10,10))
  image[1:4,4:7] = 10
  
  #==[1] Create interface class and apply the method.
  #
  improc = improcessor.basic(operator.ge,(7,))
  outIm  = improc.apply(image)
  
  print("True values where 10 values were:\n")
  print(outIm)
  
  
  #==[2] Override with new image processing: scale.
  
  scVals = np.array([0, 1])
  improc.set('processing', improcessor.basic.scale, (scVals,))
  
  outIm = improc.apply(image)
  
  print("1 values where 10 values were:\n")
  print(outIm)
  
  #==[3] Override with new image processing: scaleabout.
  
  scVals = np.array([0, 5])
  improc.set('processing', improcessor.basic.scaleabout, (scVals,))
  
  outIm = improc.apply(image)
  
  print("2.5 values where 10 values were, -2.5 values where 0 values were:\n")
  print(outIm)
  
  #==[4] Override with new image processing: normalize.
  
  improc.set('processing', improcessor.basic.normalize, ())
  
  outIm = improc.apply(image)
  
  print("1 values where 10 values were:\n")
  print(outIm)
  
  #==[5] Override with new image processing: clip.
  
  cVals = np.array([2, 8])
  improc.set('processing', improcessor.basic.clip, (cVals,))
  
  outIm = improc.apply(image)
  
  print("2/8 values where 0/10 values were:\n")
  print(outIm)


if __name__ == "__main__":
  runTest()

#
#=========================== testBasic01_usage ===========================
