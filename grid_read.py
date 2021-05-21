# -*- coding: utf-8 -*-
"""
Created on Tue May 18 13:16:56 2021

@author: Inger Grünbeck
"""
from hough_lines import transformation
import cv2
import numpy as np


class Grid:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")

        _, img = self.cap.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kernel_size = 5
        blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
        edges = cv2.Canny(blur_gray, 50, 150, apertureSize=3)

        self.start_state, self.transM, self.w, self.h = transformation(img=gray, edges=edges,
                                                                       rgb_img=None, plot_img=False)

        self.last_state = self.start_state

    def update(self, sol=False):
        _, img = self.cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        new_state = cv2.warpPerspective(gray, self.transM, (self.w, self.h))

        if sol:
            diff = (self.start_state-new_state)
        else:
            diff = (self.last_state-new_state)
            self.last_state = new_state

        x_coor = [0, int(self.w/3), int(2*self.w/3), int(self.w)]
        y_coor = [0, int(self.h/3), int(2*self.h/3), int(self.h)]
        coor = []
        th = 180

        for y in range(3):
            for x in range(3):
                m = abs(np.mean(diff[y_coor[y]:y_coor[y+1], x_coor[x]:x_coor[x+1]]))
                print(m)
                if m < th:
                    coor.append((x, y))

        if sol and len(coor) == 4:
            return coor
        elif not sol and len(coor) == 1:
            return coor[0]

    def end(self, computer_sol, player_sol):
        if not computer_sol:
            print("Congratulations!")
            print("You won!")
        elif not player_sol:
            print("Game over")
            print("You lost!")

        self.cap.release()
