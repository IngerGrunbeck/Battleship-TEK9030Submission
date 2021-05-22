# -*- coding: utf-8 -*-
"""
Created on Tue May 18 13:16:56 2021

@author: Inger Grünbeck
"""
import copy

from hough_lines import transformation
import cv2
import numpy as np


class Grid:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")

        _, image = self.cap.read()

        img = copy.deepcopy(image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kernel_size = 5
        blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
        edges = cv2.Canny(blur_gray, 50, 150, apertureSize=3)

        self.start_state, self.transM, self.w, self.h = transformation(img=gray, edges=edges,
                                                                       rgb_img=img, plot_img=True, origin_plot=False)

        self.last_state = self.start_state

    def update(self, sol=False):
        _, img = self.cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        new_state = cv2.warpPerspective(gray, self.transM, (self.w, self.h))

        if sol:
            diff = cv2.absdiff(self.start_state, new_state)
        else:
            diff = cv2.absdiff(self.last_state, new_state)
            self.last_state = new_state

        x_coor = [0, int(self.w/3), int(2*self.w/3), int(self.w)]
        y_coor = [0, int(self.h/3), int(2*self.h/3), int(self.h)]
        coor = []
        th = np.mean(diff)
        min_coor = None

        for y in range(3):
            for x in range(3):
                m = (np.mean(diff[y_coor[y]:y_coor[y+1], x_coor[x]:x_coor[x+1]]))
                if not sol:
                    if m > th:
                        min_coor = (x, y)
                        #print(m, (x,y))
                if sol:
                    if m > th:
                        coor.append((x, y))
                        #print(x,y)

        if sol and len(coor) == 4:
            return coor

        elif not sol and len(min_coor) == 2:
            return min_coor

    def end(self, computer_sol, player_sol):
        if not computer_sol:
            print("----------------")
            print("Congratulations!")
            print("You won!")
            print("----------------")
        elif not player_sol:
            print("----------------")
            print("Game over")
            print("You lost!")
            print("----------------")

        self.cap.release()
