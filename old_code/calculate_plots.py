# -*- coding: utf-8 -*-
"""
January 2017, Alexander Kutschera (alexander.kutschera@tum.de)
Script for motility assay measurement processing in python
"""

import numpy as np
import matplotlib
matplotlib.use("macosx")
from matplotlib import pyplot as plt
from pylab import savefig
from collections import OrderedDict
import math

wt = open("WT_diff.txt", "r")
mut = open("MUT_diff.txt", "r")
c1 = open("970_diff.txt", "r")
c2 = open("972_diff.txt", "r")

wt_ms = np.array([])
mut_ms = np.array([])
c1_ms = np.array([])
c2_ms = np.array([])

for line in wt:
    wt_ms = np.append(wt_ms, int(line))

for line in mut:
    mut_ms = np.append(mut_ms, int(line))

for line in c1:
    c1_ms = np.append(c1_ms, int(line))

for line in c2:
    c2_ms = np.append(c2_ms, int(line))

for i in range(len(wt_ms)):
    name = "./graphs/graph{0:04d}.png".format(i)
    x = np.arange(0, len(wt_ms[:i]))

    plt.ylim(0, 30000)
    plt.xlim(0, 300)
    plt.title("Motility 17.01.17")
    plt.ylabel("difference [pixel] (16-bit grayscale)")
    plt.plot(x, wt_ms[:i], "r-", x, mut_ms[:i], "b-", x, c1_ms[:i], "y-", c2_ms[:i], "g-")
    savefig(name, bbox_inches="tight")
