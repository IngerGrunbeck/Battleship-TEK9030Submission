# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 10:51:49 2021

@author: Inger
"""
"""
 Tested part of code 
"""
#%% import packages and image
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


sample=r'C:\Users\inger\Pictures\Camera Roll\grid_hog_opplosning.jpg'
#r'C:\Users\inger\Downloads\data-table-example1.png'
read_image= cv2.imread(sample,0)

#%% processing, threshold
convert_bin,grey_scale = cv2.threshold(read_image,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
grey_scale = 255-grey_scale
plt.figure()
plt.title('Threshold')
grey_graph = plt.imshow(grey_scale,cmap='gray')
plt.show()

#%% Find horizontal and vertical lines
length = np.array(read_image).shape[1]//100
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (length, 1))
#an opening of the structures is performed to smooth out the lines, using a line-kernel
horizontal_detect = cv2.erode(grey_scale, horizontal_kernel, iterations=3)
hor_line = cv2.dilate(horizontal_detect, horizontal_kernel, iterations=3)
plt.figure()
plt.title('Horizontal')
horizontal = plt.imshow(horizontal_detect,cmap='gray')
plt.show()

vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, length))
#an opening of the structures is performed to smooth out the lines, using a line-kernel
vertical_detect = cv2.erode(grey_scale, vertical_kernel, iterations=3)
ver_lines = cv2.dilate(vertical_detect, vertical_kernel, iterations=3)
plt.figure()
plt.title('Vertical')
vertical = plt.imshow(vertical_detect,cmap='gray')
plt.show()

#%%

final = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))#creates a rectangular kernel (2x2 array)
combine = cv2.addWeighted(ver_lines, 0.5, hor_line, 0.5, 0.0) #Adds weights to the blended images, here weighted equally
combine = cv2.erode(~combine, final, iterations=2) #invert the intensity values, and erode in order to "thicken" the lines
thresh, combine = cv2.threshold(combine,128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) #threshold the image
convert_xor = cv2.bitwise_xor(read_image,combine)
inverse = cv2.bitwise_not(convert_xor)
plt.figure()
plt.title('Detected grid')
output= plt.imshow(inverse,cmap='gray')
plt.show()

cont, _ = cv2.findContours(combine, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
def get_boxes(num, method="left-to-right"):
    invert = False
    flag = 0
    if method == "right-to-left" or method == "bottom-to-top":
        invert = True
    if method == "top-to-bottom" or method == "bottom-to-top":
        flag = 1
    boxes = [cv2.boundingRect(c) for c in num]
    (num, boxes) = zip(*sorted(zip(num, boxes),key=lambda b:b[1][flag], reverse=invert))
    return (num, boxes)
cont, boxes = get_boxes(cont, method="left-to-right")




#Correction of the boxes, eliminating the boxes significant smaller or larger than the mean

sum_3 = 0
sum_4 = 0
for element in boxes:
    sum_3 += element[-2]
    sum_4 += element[-1]
    
mean_3 = sum_3/len(boxes)
mean_4 = sum_4/len(boxes)
    
final_box = []
for box in boxes:
    s1, s2, s3, s4 = box
    if ((mean_3 - mean_3*0.2) < s3 < (mean_3 + mean_3*0.2)) and ((mean_4 - mean_4*0.2) < s4 < (mean_4 + mean_4*0.2)):
        rectangle_img = cv2.rectangle(read_image,(s1,s2),(s1+s3,s2+s4),(0,255,0),2)
        final_box.append([s1,s2,s3,s4])
        
#If not all boxes were identified, we interpolate the missing boxes
index = []
for nr, box in enumerate(final_box[1:]):
   if ((mean_4+mean_4*0.3) < abs(box[1] - final_box[nr][1]) < mean_4*5):
           index.append(nr+1)
   
if index:          
    new_rec = [int((final_box[index-1][0]+final_box[index][0])/2), 
               int(final_box[index-1][1]+mean_4), 
               int(mean_3), int(mean_4)]

    # We add the newly created boxes to the box list and image
    final_box.insert(index[0], new_rec)
    rectangle_img = cv2.rectangle(read_image,(new_rec[0],new_rec[1]),(new_rec[0]+new_rec[2],new_rec[1]+new_rec[3]),(0,255,0),2)
    
    
plt.figure()
plt.title('Final Boxes')
box_plot = plt.imshow(rectangle_img,cmap='gray')
plt.show()


#%% Not tested yet
dim = [final_box[i][3] for i in range(len(final_box))]
avg = np.mean(dim)
hor=[]
ver=[]
for i in range(len(final_box)):    
    if(i==0):
        ver.append(final_box[i])
        last=final_box[i]    
    else:
        if(final_box[i][1]<=last[1]+avg/2):
            ver.append(final_box[i])
            last=final_box[i]            
            if(i==len(final_box)-1):
                hor.append(ver)        
        else:
            hor.append(ver)
            ver=[]
            last = final_box[i]
            ver.append(final_box[i])
total = 0
for i in range(len(hor)):
    total = len(hor[i])
    if total > total:
        total = total
mid = [int(hor[i][j][0]+hor[i][j][2]/2) for j in range(len(hor[i])) if hor[0]]
mid=np.array(mid)
mid.sort()