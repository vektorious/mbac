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

path = './single_test/'

def exp_analysis():
    """ main function that will analyse the sample and generete the results data
    input
        None. It will take the frames from 'path'
    output
        None. It will generate in the process the files (JSON, CSV) with all the 
              results data.
    """
    pass

