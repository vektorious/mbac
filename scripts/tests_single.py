"""
Created on Thu May  10 2018

@authors: MBac Team

Test functions

"""

import os
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import tools_single as tools

path = './single_test/'
frames_list = []


def load_frames():
    """ auxiliary function that loads the frames in 'path' into 'frames_list'
    """
    global frames_list
    
    #create a list of filenames
    frames_list = os.listdir(path)
    
    # clean the list from unwanted files
    # only .jpg, .png, .jpeg are valid
    purged_list = []
    valid_exts = ['jpg', 'jpeg', 'png']
    for file in frames_list:
        ext = file[file.rfind('.')+1:]
        if ext in valid_exts:
            purged_list.append(file)
    frames_list = purged_list
    
    #sorting list
    frames_list.sort()
    
    return None


def test_inner_contour():
    """ displays the inner contour and the minimum circled enclosed on it
    """
    
    #testing inner contour
    
    isExit = False
    
    for frame in frames_list:
        #open the frame in grayscake
        img = cv.imread(path + frame, 0)
        
        #call detect_container from tools_single.py
        inner_cnt = tools.detect_container(img)
        
        #conver the frame to BGR
        img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
        
        #get minimin enclosing circle and draw it 
        #along with inner contour
        (x,y),radius = cv.minEnclosingCircle(inner_cnt)
        center = (int(x),int(y))
        radius = int(radius)
        cv.circle(img,center,radius,(0,255,0),1)
        cv.drawContours(img, [inner_cnt], -1, (200,0,0), 1)
        
        #display frame
        cv.imshow('image',img)
        
        # delay and 'q' key press to exit the animation
        if cv.waitKey(50) & 0xFF == ord('q'):
            isExit = True
            break
        
    while(not isExit):
        # prevent exit the display window till the user presses 'q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cv.destroyAllWindows()
    
    return None

if __name__ == '__main__':
    load_frames()