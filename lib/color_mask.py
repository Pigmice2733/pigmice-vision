"Calculate the range of the most prominent color in an image"

import cv2
import numpy as np
import json
# Turns color values into bell curve and returns local mins
from .math_extras import top_bell


def save_range(lower, upper, filename='.color_range.json'):
    """
    Given  the lower and upper color range values, write them out to filename.
    See load_range() for reading the values later.
    """
    data = {
        'lower': lower.tolist(),
        'upper': upper.tolist()
    }
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def load_range(filename='.color_range.json'):
    """
    Read a filename containing a JSON data structure that holds the upper and
    lower color range values previously calculated, calibrated, and stored.
    """
    with open(filename, 'r') as infile:
        data = json.load(infile)
        return np.array(data['lower']), np.array(data['upper'])


def color_histogram(chan):
    """
    After splitting an image into three channels (paths) of an HSV, call this
    function with one of these paths to get a _histogram_ array, where the `x`
    axis is one of 256 color values, and the `y` axis is the number of pixels
    in the image that match that value.
    """
    hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
    color_frequency = [p[0] for p in hist]

    # The numpy array (np.array) allows us to use these two demensional array
    return np.array(color_frequency)


def image_colors(image):
    """
    Returns a list of three histogram arrays, one for each of the HSV channels
    in the image given.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Split into the three channels of hue, saturation, and value.
    # We then initialize a tuple of strings representing the colors.
    chans = cv2.split(hsv)

    return [color_histogram(chan) for chan in chans]


def color_range(image):
    """
    Smooth values (from graph.py) and with max_peak_deviation finds the most
    frequent colors as a list of two values that form a _range_ of the most
    prominent color in image.

    It does this by making a bell curve from the images' most frequently used
    color, as well as its neighbors, by sloping downwards on both sides to the
    curve's local mins.
    """
    min_color = []
    max_color = []

    for hist_channel in image_colors(image):
        l, u = top_bell(smooth(hist_channel))
        # The standard deviation creates too small of a range, about 50 is
        # needed to be added and subtracted from the min and max values to
        # account for changes in light
        min_color.append(l)
        max_color.append(u)

    lower = np.asarray(min_color)  # Able to use two demensional array
    upper = np.asarray(max_color)

    return(lower, upper)  # returns lowest and highest most frequent values


# Collection of functions that work on 1D datasets and help with displaying
# those datasets in graph form.
#
# The smoothing feature was taken from this SciPy Cookbook chapter:
# http://scipy-cookbook.readthedocs.io/items/SignalSmooth.html


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

    return np.convolve(w/w.sum(), s, mode='valid')
