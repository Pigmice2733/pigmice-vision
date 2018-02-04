"Math related functions that extend numpy."

import numpy as np


def local_min_max(data):
    """
    Return two arrays of the 'x' values (think index into the data array),
    where the first array contains the positions of all local minimums, and the
    second array contains all local maximums.
    """
    mins = (np.diff(np.sign(np.diff(data))) > 0).nonzero()[0] + 1  # local min
    maxs = (np.diff(np.sign(np.diff(data))) < 0).nonzero()[0] + 1  # local max
    return [mins, maxs]


def top_bell(data):
    """
    Return the index (x value) of the local minimum values surrounding the
    absolute maximum in a sequence... the range of the top peak of a bumpy
    curve values.
    """
    maxn = np.argmax(data)     # The maximum value (y position)
    mins, _ = local_min_max(data)
    smaller = list(filter(lambda i: i < maxn, mins))
    larger = list(filter(lambda i: i > maxn, mins))
    return smaller[-1], larger[0]


def __find_in_range(seq, value, index_range):
    """
    Given an index_range (created with the `range` function), return the index
    of the first number that is less than the values specified.

    Note: Throws an Exception if not found.
    """
    for idx in index_range:
        if seq[idx] < value:
            return idx
    raise Exception("Value, {}, not found in sequence.".format(value))


def __get_lower_index(seq, value, start):
    """
    Returns the index in `seq`uence of the first value _before_ start that is
    less than value.
    """
    return __find_in_range(seq, value, range(start, 0, -1))


def __get_upper_index(seq, value, start):
    """
    Returns the index in `seq`uence of the first value _after_ start that is
    less than value.
    """
    return __find_in_range(seq, value, range(start + 1, len(seq)))


def max_peak_deviation(seq):
    """
    Return two `y` values associated with the standard deviation from the
    maximum x value in the sequence:

        lower_y, upper_y = max_peak_deviation(seq)

    Care about the actual x value of each of these two points? Get these via:

        lower_x = seq[lower_y]
        upper_y = seq[upper_y]
    """
    max_x = np.max(seq)
    max_y = np.argmax(seq)

    # Calculate a bell curve from the max value:
    begin, end = top_bell(seq)
    bell = seq[begin:end]

    # Calculate the standard `x` value of the standard deviation.
    # Note that this value will be less than the max value, and it
    # is really a _goal_, and may not actually exist in our seq:
    dev_x_goal = max_x - np.std(bell)/2

    # Loop up and down the sequence from the max value, looking for the first
    # entry that is less than our standard deviation goal:
    low_point_y = __get_lower_index(seq, dev_x_goal, max_y)
    up_point_y = __get_upper_index(seq, dev_x_goal, max_y)

    return [low_point_y, up_point_y]
