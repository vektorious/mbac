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
    name = "./el_bgraphs/el_bgraph{0:04d}.png".format(i)

    if i <= 9:
        start = 0
    else:
        start = i - 10

    wt_el = (wt_ms[i] - wt_ms[(start)])/10
    mut_el = (mut_ms[i] - mut_ms[(start)])/10
    c1_el = (c1_ms[i] - c1_ms[(start)])/10
    c2_el = (c2_ms[i] - c2_ms[(start)])/10

    N = 4

    fig, ax = plt.subplots()
    ind = np.arange(N)
    width = 0.3
    ax.set_ylim(0, 250)
    ax.set_title("Motility 17.01.17")
    ax.set_ylabel("slope (over last 10 ms points)")
    ax.bar(0+width, wt_el, width, color="red")
    ax.bar(1+width, mut_el, width, color="blue")
    ax.bar(2+width, c1_el, width, color="yellow")
    ax.bar(3+width, c2_el, width, color="green")
    ax.set_xticks(ind + 1.5*width)
    ax.set_xticklabels(("WT", "Mut", "L970", "L972"))
    fig.savefig(name, bbox_inches="tight")
    plt.close(fig)
