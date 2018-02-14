#!/usr/bin/env python
"""Test the functions in the lib/graph file.

This test program can also run as a stand-alone application
to demonstrate visually how the smooth function can work.
"""

from context import lib  # flake8: noqa
from lib import color_mask
import numpy as np
from numpy.random import randn
import matplotlib.pyplot as plt

def test_smooth_hanning():
    """
    Take a series of numbers along a slope, and verify that the hanning function
    returns expected values. This really tests that the system works correctly more
    than testing the Hanning algorithm itself.
    """
    data = np.array([-0.6, 0.0, -0.6, -1.0, -0.4, 0.1, 0.6, 1.0, 0.4, 0.0, 0.4])
    expected = np.array([0.0, -0.6, 0.0, -0.6, -1.0, -0.4, 0.1, 0.6, 1.0, 0.4, 0.0, 0.4, 0.0])
    y = color_mask.smooth(data, 3, 'hanning')
    assert np.array_equiv(y, expected)


def test_slope_to_curve():
    """
    Keep in mind the smoothing function assumes some sort of sine-line wave, so
    a simple slope won't work as expected. This test is really a demonstration
    of its behavior, but validates that the system is working correctly.
    """
    data = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    expected=np.array([1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 5.0])
    y = color_mask.smooth(data, 3)
    assert np.array_equal(y, expected)


def smooth_demo():
    """
    This demonstration creates a series of numbers along a sine curve, and then
    slightly shifts those numbers randomly to create some variation. We can then
    display this array along with the curves returned from our smoothing function
    to see how each behaves.
    """
    t = np.linspace(-4, 4, 100)
    x = np.sin(t)
    xn = x + randn(len(t)) * 0.1
    y = color_mask.smooth(x)
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
        plt.plot(color_mask.smooth(xn,10,w))
    l=['original signal', 'signal with noise']
    l.extend(windows)

    plt.legend(l)
    plt.title("Smoothing a noisy signal")
    plt.show()


if __name__=='__main__':
    smooth_demo()
