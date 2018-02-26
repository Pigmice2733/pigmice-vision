"Calculate the range of the most prominent color in an image"

import cv2
import numpy as np
from .math_extras import top_bell


def pack_range(lower, upper):
    """
    Takes lower and upper color range values and packs them in a dictionary.
    """
    return {
        "lower": lower.tolist(),  # tolist converts numpy array into a regular
        "upper": upper.tolist()  # array that the dictionary can use
    }


def unpack_range(d):
    """
    Takes the dictionary in pack_range and converts them to individual
    numpy arrays.
    """
    lower = np.array(d["lower"])
    upper = np.array(d["upper"])
    return lower, upper


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
    chans = cv2.split(hsv)

    return [color_histogram(chan) for chan in chans]


def color_range(image):
    """
    Smooth values and find the bell curve of the most frequent color.
    The lower and upper ranges are found from the minimum and maximum values
    in this bell curve.
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


def get_mask(hsv_img, lower, upper):
    """
    Given an image and color range, return a simplified masked image.
    """
    thresh = cv2.inRange(hsv_img, lower, upper)

    # perform some clean up before contour operations
    # thresh = cv2.erode(thresh, None, iterations=2)
    # thresh = cv2.dilate(thresh, None, iterations=2)

    return thresh


def get_contours(img):
    """
    Contours are a curve joining all the continuous points along the
    boundary of the same color or intensity. The list of contours are
    sorted based on size from smallest to largest.
    """
    # _ = image that is ignored
    _, contours, hierarchy = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL,
                                              cv2.CHAIN_APPROX_SIMPLE)
    return sorted(contours, key=cv2.contourArea)


def double_target(img):
    """
    Logic to find the center of two objects, such as two pieces of vision tape.
    Returns center of object (x,y coordinate on image frame), size,
    and orientation of object.
    """
    pass

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

