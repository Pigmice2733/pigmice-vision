"""
Collection of functions that work on 1D datasets and help with displaying
those datasets in graph form.

The smoothing feature was taken from this SciPy Cookbook chapter:
http://scipy-cookbook.readthedocs.io/items/SignalSmooth.html
"""

import numpy as np


def smoothing_moving_avg(x):
    "Making a flat smoothing window average requires an array of ones."
    return np.ones(x, 'd')


def smoothing_func(window_type):
    """Since we have many ways of smoothing values in a data series, let's have a
    dispatch function that takes the algorithmic style as a string, and returns
    the appropriate function we could call.

    input:
        window_type: the type of window from 'flat', 'hanning', 'hamming',
            'bartlett', 'blackman' flat window will produce a moving average
            smoothing.

    output:
        the smoothing function
    """
    # We could raise an error if the window type is not entered correctly, ala:
    if window_type not in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window type is not one of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    # Or we could just use a default value of 'flat' ...
    return {
        'hanning': np.hanning,
        'hamming': np.hamming,
        'bartlett': np.bartlett,
        'blackman': np.blackman
    }.get(window_type, smoothing_moving_avg)


def smooth(x, window_len=11, window='hanning'):
    """smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal (with
    the window size) in both ends so that transient parts are minimized in the
    begining and end part of the output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window; an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming',
            'bartlett', 'blackman' flat window will produce a moving average
            smoothing.

    output:
        the smoothed signal

    example:

    t = linspace(-2,2, 0.1)
    x = sin(t) + randn(len(t)) * 0.1
    y = smooth(x)

    see also:

    np.hanning, np.hamming, np.bartlett, np.blackman,
    np.convolve, scipy.signal.lfilter

    NOTE: length(output) != length(input), to correct this:
          return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """
    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")
    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")
    if window_len < 3:
        return x

    sf = smoothing_func(window)
    s = np.r_[x[window_len-1:0:-1], x, x[-2:-window_len-1:-1]]
    w = sf(window_len)

    # print(len(s))
    return np.convolve(w/w.sum(), s, mode='valid')
