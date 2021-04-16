# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 16:53:38 2021

@author: Inger
"""

import matplotlib.pyplot as plt
import PySimpleGUI as sg

image  = plt.imread(r"C:\Users\inger\Pictures\Camera Roll\grid.jpg")
plt.imshow(image, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()

print('press enter in order to close window and continue')
plt.waitforbuttonpress()
plt.close()



sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Press enter to continue')],
            [sg.Button('Continue')]
             ]

# Create the Window
window = sg.Window('Game setup', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Continue': # if user closes window or clicks cancel
        break
window.close()
    


