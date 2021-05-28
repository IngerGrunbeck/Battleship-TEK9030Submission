# -*- coding: utf-8 -*-
"""
Created on Tue May 18 2021

@author: Inger Grünbeck (inger.gruenbeck@gmail.com)
Project: TEK9030 - Implementing Battleship

Code partially based on [1].

[1]: Adrian Rosebrock. "4 Point OpenCV getPerspective Transform Example".
    URL: https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
    Accessed: (20.05.2021)
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt


def intersection(line1, line2):
    x1, y1, x2, y2 = line1[0], line1[1], line1[2], line1[3]
    a1 = y2 - y1
    b1 = x1 - x2
    c1 = b1*y1 + a1*x1
    
    x1, y1, x2, y2 = line2[0], line2[1], line2[2], line2[3]
    a2 = y2 - y1
    b2 = x1 - x2
    c2 = b2*y1 + a2*x1
    
    det = a1*b2 - a2*b1
    
    if det == 0:
        return None
    else:
        return int((b2*c1 - b1*c2)/det), int((a1*c2 - a2*c1)/det)


def transformation(img, edges, rgb_img=None, plot_img=False, origin_plot=False):
    # The parameters for the Hough line detection
    rho = 1
    theta = np.pi / 180
    threshold = 15
    min_line_length = 130
    max_line_gap = 70
        
    # Run Hough line transform on the canny-processed image,
    # detecting line segments in the image based on the given parameters
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)
    
    # Differ between vertical and horizontal lines
    vertical_lines = []
    horizontal_lines = []
    for element in lines:
        un = np.squeeze(element)
        if abs(un[2]-un[0]) < 40:
            vertical_lines.append(un)
        elif abs(un[3]-un[1]) < 40:
            horizontal_lines.append(un)
            
    # Finding intersections between vertical and horizontal lines
    # Intersections outside of the image's size are excluded
    inter = []
    for ho_line in horizontal_lines:
        for ve_line in vertical_lines:
            x, y = intersection(ho_line, ve_line)
            if x and (x < img.shape[1]) and (y < img.shape[0]):
                inter.append([x, y])
     
    # Identify the grid's main corners
    inter = np.array(inter)
    pts1 = np.zeros((4, 2), dtype="float32")
    s = inter.sum(axis=1)
    pts1[0] = inter[np.argmin(s)]
    pts1[2] = inter[np.argmax(s)]
    
    d = np.diff(inter, axis=1)
    pts1[1] = inter[np.argmin(d)]
    pts1[3] = inter[np.argmax(d)]
        
    # Construct a new image containing the copped grid
    wa = np.sqrt((pts1[2][0]-pts1[3][0])**2 + (pts1[2][1]-pts1[3][1])**2)
    wb = np.sqrt((pts1[1][0]-pts1[0][0])**2 + (pts1[1][1] - pts1[0][1])**2)
    maxw = max(int(wa), int(wb))
    
    ha = np.sqrt((pts1[1][0]-pts1[2][0])**2 + (pts1[1][1]-pts1[2][1])**2)
    hb = np.sqrt((pts1[0][0]-pts1[3][0])**2 + (pts1[0][1]-pts1[3][1])**2)
    maxh = max(int(ha), int(hb))
    
    pts2 = np.array([[0, 0], [maxw-1, 0], [maxw-1, maxh-1], [0, maxh-1]], dtype='float32')

    # Calculate the homography and transform the image
    mtx = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(img, mtx, (maxw, maxh))

    # Print detected lines and intersections if origin_plot = True
    # Print the cropped grid if plot_image = True
    if plot_img:
        point_image = np.copy(rgb_img) * 0            
        for coor in pts1:
            point_image[int(coor[1]), int(coor[0]), :] = [0, 255, 0]
        
        line_image = np.copy(rgb_img) * 0
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)
        lines_edges = cv2.addWeighted(rgb_img, 0.8, line_image, 0.8, 0)
        points = cv2.addWeighted(lines_edges, 0.6, point_image, 1, 0)

        if origin_plot:
            plt.figure()
            plt.imshow(points, cmap='gray')
            plt.show()
        
        plt.figure()
        plt.imshow(dst, cmap='gray')
        plt.show()
        
    return dst, mtx, maxw, maxh
