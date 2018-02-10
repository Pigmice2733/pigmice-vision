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

    # If the lowest or highest value is the very highest or lowest value it
    # won't account for it, so we have to add 0 and the length of the data to
    # put in those values just in case
    full_mins = np.insert(mins, 0, 0)  # Insert a 0 into the list's [0] spot
    full_mins = np.append(full_mins, len(data)-1)
    return [full_mins, maxs]


def top_bell(data):
    """
    Return the index (x value) of the local minimum values surrounding the
    absolute maximum in a sequence... the range of the top peak of a bumpy
    curve values.
    """
    max_y = np.max(data)
    max_x = np.argmax(data)  # The maximum value (x position)
    mins, maxs = local_min_max(data)
    smaller = list(filter(lambda i: i < max_x, mins))
    larger = list(filter(lambda i: i > max_x, mins))
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
        upper_x = seq[upper_y]
    """

    # Calculate a bell curve from the max value:
    begin, end = top_bell(seq)

    # lowest and highest values on the cropped data set in the bell curve
    return [begin, end]
    # To return the lowest and highest standard deviation:
    # return [low_point_y, up_point_y]

    # To Calulate the lowest and highest standard deviation values:
    #    max_x = np.max(seq)
    #    max_y = np.argmax(seq)

    #   bell = seq[begin:end]

    #   low_point_y = __get_lower_index(seq, dev_x_goal, max_y)
    #   up_point_y = __get_upper_index(seq, dev_x_goal, max_y)
