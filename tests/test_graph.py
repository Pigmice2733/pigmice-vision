#!/usr/bin/env python
"""Test the functions in the lib/graph file.

This test program can also run as a stand-alone application
to demonstrate visually how the smooth function can work.
"""

from context import lib  # flake8: noqa
from lib import util
import numpy as np
from numpy.random import randn
import matplotlib.pyplot as plt

def test_smooth_hanning():
    "Assume we "


def smooth_demo():
    t = np.linspace(-4, 4, 100)
    x = np.sin(t)
    xn = x + randn(len(t)) * 0.1
    y = smooth(x)
    ws = 31

    # Top Graph:
    plt.subplot(211)
    plt.plot(np.ones(ws))

    windows=['flat', 'hanning', 'hamming', 'bartlett', 'blackman']

    plt.hold(True)
    for w in windows[1:]:
        eval('plt.plot(np.'+w+'(ws) )')
    plt.axis([0,30,0,1.1])
    plt.legend(windows)
    plt.title("The smoothing windows")

    # Bottom Graph:
    plt.subplot(212)
    plt.plot(x)
    plt.plot(xn)
    for w in windows:
        plt.plot(smooth(xn,10,w))
    l=['original signal', 'signal with noise']
    l.extend(windows)

    plt.legend(l)
    plt.title("Smoothing a noisy signal")
    plt.show()


if __name__=='__main__':
    smooth_demo()
