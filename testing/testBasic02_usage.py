#=========================== testBasic02_usage ===========================
#
# @brief    Code to create an image interface and then use it to process
#           the source image. Uses openCV resize function.
#
#=========================== testBasic02_usage ===========================

#
# @file     testBasic02_usage.py
#
# @author   Yunzhi Lin, yunzhi.lin@gatech.edu
# @date     2021/07/07 [created]
#
#!NOTE:
#!  Indent is set to 2 spaces.
#!  Tab is set to 4 spaces with conversion to spaces.
#
# @quit
#=========================== testBasic02_usage ===========================

#==[0] Prep environment
#
import cv2

Image = cv2.imread('lena.png')
newImage_list = []

#==[1] Create the interface class, you can also try any opencv functions based on the needs
#
improc = improcessor.basic(cv2.resize,((400,10),),\
                           improcessor.basic.clip,((2,100),))

#==[2] Apply the methods
#
newImage_list.append(improc.apply(Image))

#==[3] Reset the methods
#
improc.set('processing',improcessor.basic.clip,((2,20),)])
newImage_list.append(improc.apply(Image))

#==[4] Directly apply the builtin methods
#
newImage_list.append(improcessor.basic.clip(Image, (2,20)))

#==[5] Display the methods
#
print(improc.get('processing'))

#==[6] Display the results
#
for i in range(len(newImage_list)):
  if newImage_list[i] is not None:
    cv2.imshow('Demo',newImage_list[i])
    cv2.waitKey()
  else:
    print('Error found!')


#
#=========================== testBasic02_usage ===========================
