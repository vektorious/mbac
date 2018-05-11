"""
Created on Thu May  10 2018

@authors: MBac Team

A function that will be run to analyze all the experiment sample, 
making use of tools_single.py in every frame.
It also generates results.json(.csv) files where the analysis data
(area and velocity) are saved.

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


def exp_analysis():
    """ main function that will analyse the sample and generete the results data
    input
        None. It will take the frames from 'path'
    output
        None. It will generate in the process the files (JSON, CSV) with all the 
              results data.
    """
    pass




def tests():
    """ developing tests 
    """
    pass


