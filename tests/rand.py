import numpy as np
import math
import matplotlib.pyplot as plt


def plot(ary, label="Array Values", marks=[]):
    """
    Simple function to visually display an array of numbers.
    """
    plt.plot(ary)
    plt.ylabel(label)
    if len(marks) > 0:
        for m in marks:
            plt.axvline(x=m)
    plt.show()


def shift_to_zero(ary):
    """
    Adds a number to every value in the given array such that the
    lowest number is 0, and all other numbers are greater than that.
    """
    lowest = np.min(ary)
    increase = np.vectorize(lambda n: n + abs(lowest))
    return increase(ary)


def scale_to_100(ary):
    """
    Multiplies every element in the array given by a number that
    will scale all numbers _close to_, but not greater than 100.
    """
    highest = np.max(ary)
    factor = 100 / math.ceil(highest)
    scale = np.vectorize(lambda n: n * factor)
    return scale(ary)


def bell_sort(ary):
    """
    Sorts an array where the largest value is in moved to the
    middle of the array, and the lowest values are towards the
    first and end of the array. For an array of linear values,
    this would result in a triangular looking array, however,
    with a normal distribution, this should resemble a
    standard bell curve.
    """
    mid = ary.size // 2

    # Sort changes the array, and doesn't return the new sorted array,
    # so we to create two new arrays, first and second halves:
    f_half = ary[0:mid]
    s_half = ary[mid:]
    f_half.sort()
    s_half.sort()

    # Combine the two arrays with append, but reverse the order
    # of the second half with the flip function:
    return np.append(f_half, np.flip(s_half, axis=-1))


def random_bell(size=10):
    """
    Generate a array of random numbers of the size given, but
    order the numbers along a bell curve with values ranging
    from 0 up to 100.
    """
    v = np.random.normal(size=size)
    nums = scale_to_100(shift_to_zero(v))
    return bell_sort(nums).astype(int)


def random_bumpy_peak(size=1000):
    """
    Generates an array of random numbers with a single maximum peak (near the
    center), and a number of lower peaks and valleys, with more closely
    resembles a single channel from a color histogram. Look for multiple
    maximums and minimums.
    """
    x = np.linspace(0, 4, size)  # Generates a straight line of data points
    return .2*np.sin(10*x) + np.exp(-abs(2-x)**2)


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


def demo1():
    seq = random_bell()
    maxn = np.max(seq)     # The maximum value (y position)
    maxi = np.argmax(seq)  # The maximum value's index (x position)

    point1_y = maxn - np.std(seq)/2
    point2_y = maxn + np.std(seq)/2
    rng = [
           maxn + np.std(seq)/2]
    plot(seq, marks=[4, 8])
    print(maxi)


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


def demo2():
    seq = random_bumpy_peak()

    print("Here is a curve where we have mapped the top peak.")
    begin, end = top_bell(seq)
    plot(seq, marks=[begin, end])

    # print("here is that top curve peak displayed by itself.")
    bell = seq[begin:end]
    # plot(bell)

    print("Here is the standard deviation of the top peak.")
    max_x = np.max(bell)
    point1_x = max_x - np.std(bell)/2
    point2_x = max_x - np.std(bell)/2

    max_y = np.argmax(seq)
    point1_y = __get_lower_index(seq, point1_x, max_y)
    point2_y = __get_upper_index(seq, point2_x, max_y)

    print(point1_x, point1_y, max_x, max_y, point2_x, point2_y)
    plot(seq, marks=[point1_y, point2_y])


if __name__ == '__main__':
    """
    How can we get the index values of the standard deviation from a sequences
    maximum, but between two local mimimums?
    """
    demo2()
# that's the line, you need:


# graphical output...
# from pylab import *
# plot(x,data)
# plot(x[b], data[b], "o", label="min")
# plot(x[c], data[c], "o", label="max")
# legend()
# show()
