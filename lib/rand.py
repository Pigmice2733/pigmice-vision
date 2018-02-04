import numpy as np
import math
import matplotlib.pyplot as plt


def plot(ary, label="Frequency", marks=[]):
    """
    Simple function to visually display an array of numbers.

    The marks is an array of `y` values that will be highlighted with a
    vertical bar.
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
