# -*- coding: utf-8 -*-
"""
Created on Tue May 18 13:16:56 2021

@author: Inger

insp:
https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
https://stackoverflow.com/questions/45322630/how-to-detect-lines-in-opencv
https://aishack.in/tutorials/solving-intersection-lines-efficiently/

"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import copy

def intersection(line1, line2):
    x1, y1, x2, y2 = line1[0], line1[1], line1[2], line1[3]
    A1 = y2 - y1
    B1 = x1 - x2
    C1 = B1*y1 + A1*x1
    
    x1, y1, x2, y2 = line2[0], line2[1], line2[2], line2[3]
    A2 = y2 - y1
    B2 = x1 - x2
    C2 = B2*y1 + A2*x1
    
    det = A1*B2 - A2*B1
    
    if det == 0:
        return None
    else:
        return int((B2*C1 - B1*C2)/det), int((A1*C2 - A2*C1)/det)

def transformation(rgb_img, img, edges, plot_img=False):
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 120  # maximum gap in pixels between connectable line segments
        
    # Run Hough on edge detected image
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)
    
    # Differ between vertical and horizontal lines
    vertical_lines = []
    horizontal_lines = []
    
    for  element in lines:
        un = np.squeeze(element)
        if abs(un[2]-un[0]) < 40:
            vertical_lines.append(un)
        elif abs(un[3]-un[1]) < 40:
            horizontal_lines.append(un)
        else: 
            print(un)
            
    # Finding intersections between vertical and horizontal lines        
    inter = []
    for ho_line in horizontal_lines:
        for ve_line in vertical_lines:
            x,y = intersection(ho_line, ve_line)
            if x:
                inter.append([x,y])
     
    # Identify the outerpoints of the grid's main corners
    inter = np.array(inter)
    pts1 = np.zeros((4, 2), dtype = "float32")
    s = inter.sum(axis=1)
    pts1[0] = inter[np.argmin(s)]
    pts1[2] = inter[np.argmax(s)]
    
    d = np.diff(inter, axis = 1)
    pts1[1] = inter[np.argmin(d)]
    pts1[3] = inter[np.argmax(d)]
        
    # Construct new defined grid
    wA = np.sqrt((pts1[2][0]-pts1[3][0])**2 + (pts1[2][1]-pts1[3][1])**2)
    wB = np.sqrt((pts1[1][0]-pts1[0][0])**2 + (pts1[1][1] - pts1[0][1])**2)
    maxW = max(int(wA), int(wB))
    
    hA = np.sqrt((pts1[1][0]-pts1[2][0])**2 + (pts1[1][1]-pts1[2][1])**2)
    hB = np.sqrt((pts1[0][0]-pts1[3][0])**2 + (pts1[0][1]-pts1[3][1])**2)
    maxH = max(int(hA), int(hB))
    
    pts2 = np.array([[0,0], [maxW-1, 0], [maxW-1, maxH-1], [0, maxH-1]], dtype='float32')
    
    
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(img,M,(maxW,maxH))
    
    if plot_img == True:
        # Print lines and points   as part of image      
        point_image = np.copy(rgb_img) * 0            
        for coor in pts1:
            point_image[int(coor[1]), int(coor[0]), :] = [0,0,255]
        
        line_image = np.copy(rgb_img) * 0
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)
        lines_edges = cv2.addWeighted(rgb_img, 0.8, line_image, 1, 0)
        points = cv2.addWeighted(lines_edges, 0.8, point_image, 1, 0)    
        
        plt.figure(); plt.imshow(points); plt.show()
        
        plt.figure(); plt.imshow(dst); plt.show()
        
    return dst, M, maxW, maxH

if __name__ == "__main__":
    camera = True
    
    if camera==True:
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise IOError("Cannot open webcam")
            
        _, image = cap.read()
    
    else:
        file_path = r'C:\Users\inger\Pictures\Camera Roll\WIN_20210518_15_27_26_Pro.jpg'
        image = cv2.imread(file_path)
     
    # Preprocess image
    img = copy.deepcopy(image)
    start_state = None
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)
    edges = cv2.Canny(blur_gray,50,150,apertureSize = 3)
    
    if start_state is None:
        start_state, transM, w, h = transformation(rgb_img=img, img=gray, edges=edges, plot_img=True)
    else:
        new_state = cv2.warpPerspective(img,transM,(w,h))
    
    last_state=new_state
    #if camera==True:
    #    cap.release()
    
    
