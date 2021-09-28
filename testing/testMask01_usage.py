#!/usr/bin/python3
#========================= testMask01_usage =========================
#
# @brief    Test the functionality of the mask operators with a 
#           sample binary image
#
#========================= testMask01_usage =========================
#
# @file     testMask01_usage.py
#
# @author   Yiye Chen,          yychen2019@gatech.edu
# @date     2021/09/28
#
#!NOTE:
#!  Indent is set to 2 spaces.
#!  Tab is set to 4 spaces with conversion to spaces.
#
#========================= testMask01_usage =========================

#==[0] environment
import improcessor.mask as maskproc
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import sys

fPath = os.path.dirname(os.path.abspath(__file__))

#==[1] input data
mask = cv2.imread(os.path.join(fPath, "binary_i.png"), cv2.IMREAD_GRAYSCALE)
mask = (mask > 1)

#==[2] Define a sequence of operation
kernel = np.ones((5,5), dtype=bool)
proc = maskproc.mask(
    maskproc.mask.getLargestCC, (),
    maskproc.mask.erode, (kernel, ),
    maskproc.mask.dilate, (kernel, )
)
proc.apply(mask, cache=True)

#==[3] Visualization
print("The processing sequence: \n {} \n".format(proc.get("processing")))
masks = proc.get_cache_results()
fig, axes = plt.subplots(1, 4)
axes[0].imshow(mask, cmap="gray")
axes[0].set_title("Initial Mask")
for i in range(len(masks)):
    axes[i+1].imshow(masks[i], cmap="gray")
    axes[i+1].set_title("Process Step {}".format(i+1))

plt.show()