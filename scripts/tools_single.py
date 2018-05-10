#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  10 2018

@authors: MBac Team

Set of tools that will allow the image recognition in the experiments

"""

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def detect_container(img):
    """ detects the inner boundary of the petridish in an image
    input
        img: grayscale image as numpy array
    ouput: 
        cntr: an opencv contour object representing the inner border 
              of the petridish
    """
    
    pass

def create_ROI(img, cntr):
    """ creates a mask displaying only the region inside cntr in the image 
    input
        img: grayscale image as numpy array
        cntr: opencv contour object representing the inner border 
              of the petridish
    output
        ROI: a binary mask (black/white), numpy array, representing the area inside 
             the petridish
    """
    
    pass

def calc_brightRange(img, ROI):
    """ calculates mimimum and maximum grayscale value inside the petridish empty area
    input
        img: grayscale image as numpy array
        ROI: a binary mask (black/white), numpy array, representing the are inside 
             the petridish
    output
        (minValue,maxValue): grayscale values (0-255) that apears in the empy area
                             of a petridish
    """
    pass

def detect_bacteria(img, ROI, minValue, maxValue):
    """ finds the bacteria region
    input
        img: grayscale image as numpy array
        ROI: a binary mask (black/white), numpy array, representing the are inside 
             the petridish
        (minValue,maxValue): grayscale values (0-255) that apears in the empy area
                             of a petridish
    output
        bac_cntrs: a list of openCV contour objects representing the bacteria's region'
    """
    pass

def calc_area(cntrs):
    """ calculate the total area inside all the contours
    input
        cntrs: a list of openCV contour objects representing the bacteria's region
    output
        total_area: a float number that indicates the total number of pixels inside
                    all the contours 
    """
    pass
